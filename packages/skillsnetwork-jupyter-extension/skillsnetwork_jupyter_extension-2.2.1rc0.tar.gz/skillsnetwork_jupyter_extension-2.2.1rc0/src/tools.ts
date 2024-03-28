/* eslint-disable @typescript-eslint/ban-types */
import { AxiosError } from 'axios';
import { Cell, ICellModel } from '@jupyterlab/cells';
import { INotebookModel, NotebookPanel } from '@jupyterlab/notebook';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { IDefaultFileBrowser } from '@jupyterlab/filebrowser';
import { Contents } from '@jupyterlab/services';
import * as nbformat from '@jupyterlab/nbformat';
import { Dialog, showDialog } from '@jupyterlab/apputils';
import { PathExt } from '@jupyterlab/coreutils/lib/path';
import { ENV_TYPE, EnvType, Globals } from './config';
import {
  atlasAxiosHandler,
  getLabModel,
  awbAxiosHandler,
  getIndependentLabModel,
  getLearnerLabModel
} from './handler';

export interface ICellData {
  cell_type: string;
  id: string;
  metadata: {};
  outputs: [];
  source: string[];
}
export interface IPynbRaw {
  cells: ICellData[];
  metadata: {};
  nbformat: number;
  nbformat_minor: number;
}

/**
 * Extracts the relevant data from the cells of the notebook
 *
 * @param cell Cell model
 * @returns ICellData object
 */
export const getCellContents = (cell: Cell<ICellModel>): ICellData => {
  const source = cell.model.toJSON().source;
  const sourceArray: string[] = typeof source === 'string' ? [source] : source;
  const cellData: ICellData = {
    cell_type: cell.model.type,
    id: cell.model.id,
    metadata: {},
    outputs: [],
    source: sourceArray
  };
  return cellData;
};

/**
 * Extracts the relevant data from the cells of the notebook but omit ID
 *
 * @param cell Cell model
 * @returns ICellData object without ID
 */
export const getCellContentsOmitID = (cell: Cell<ICellModel>): ICellData => {
  const source = cell.model.toJSON().source;
  const sourceArray: string[] = typeof source === 'string' ? [source] : source;
  const cellData: ICellData = {
    cell_type: cell.model.type,
    id: '',
    metadata: {},
    outputs: [],
    source: sourceArray
  };
  return cellData;
};

/**
 * Gets the raw data (cell models and content, notebook configurations) from the .ipynb file
 *
 * @param panel Notebook panel
 * @param context Notebook context
 */
export const getFileContents = (
  panel: NotebookPanel,
  context: DocumentRegistry.IContext<INotebookModel>
): string => {
  // Cell types: "code" | "markdown" | "raw"
  const allCells: any[] = [];
  panel.content.widgets.forEach((cell: Cell<ICellModel>) => {
    const cellData = getCellContents(cell);
    allCells.push(cellData);
  });

  const config_meta = {
    kernelspec: context.model.getMetadata('kernelspec'),
    language_info: context.model.getMetadata('language_info'),
    orig_nbformat: context.model.getMetadata('orig_nbformat'),
    [Globals.PREV_PUB_HASH]: context.model.getMetadata(Globals.PREV_PUB_HASH)
  };
  const config_nbmajor = context.model.nbformat;
  const config_nbminor = context.model.nbformatMinor;

  // Put all data into IPynbRaw object
  const rawFile: IPynbRaw = {
    cells: allCells,
    metadata: config_meta,
    nbformat: config_nbmajor,
    nbformat_minor: config_nbminor
  };
  return JSON.stringify(rawFile, null, 2);
};

/**
 * Ensures the subfolders exist for the given filename by creating them if they don't.
 *
 * @param docManager the JupyterLab document manager
 * @param filename the filename to ensure the subfolders exist for
 */
export const ensureSubFoldersExist = async (
  docManager: IDocumentManager,
  filename: string
): Promise<void> => {
  filename = PathExt.removeSlash(filename);
  const dirname = PathExt.dirname(filename);
  const paths: string[] = [];
  dirname.split('/').reduce((prev, item) => {
    const path = PathExt.removeSlash(prev + '/' + item);
    paths.push(path);
    return path;
  }, '');

  console.log(paths);

  for (const dir of paths) {
    try {
      await docManager.services.contents.get(dir, { content: false });
    } catch (e) {
      console.log('Creating', dir);
      const dirModel = await docManager.newUntitled({
        path: '',
        type: 'directory'
      });

      await docManager.rename(dirModel.path, dir);
    }
  }
};

/**
 * Updates the file with its commit ID
 *
 * @param panel Notebook panel
 * @param context Notebook context
 */
export async function updateLabCommitID(
  panel: NotebookPanel,
  context: DocumentRegistry.IContext<INotebookModel>
): Promise<void> {
  const fileCells: string = await getFileCellContentsOmitID(panel, context);
  const commitID = await generateHash(fileCells);

  await context.ready;

  context.model.setMetadata(Globals.PREV_PUB_HASH, commitID);

  // Save the notebook to persist the changes
  context
    .save()
    .then(() => {
      console.log('Notebook saved with updated commit ID.');
    })
    .catch(err => {
      console.error('Failed to save notebook with updated commit ID:', err);
    });
}

/**
 * Defines the expected structure of lab content.
 */
interface ILabContent {
  metadata?: {
    [key: string]: string | object | undefined;
  };
  content?: {
    metadata?: {
      [key: string]: string | object | undefined;
    };
  };
}

/**
 * Updates the file with its commit ID
 *
 * @param panel Notebook panel
 * @param context Notebook context
 */
export function getLabCommitID(labContent: ILabContent): string {
  if (typeof labContent === 'string') {
    labContent = JSON.parse(labContent);
  }
  if (
    typeof labContent !== 'object' ||
    labContent === null ||
    (!('metadata' in labContent) && !('content' in labContent))
  ) {
    console.error(
      'Lab content is of unknown type: ',
      typeof labContent,
      '\n Value: \n',
      labContent
    );
    return '';
  }

  const commitID =
    labContent.metadata?.[Globals.PREV_PUB_HASH]?.toString() ??
    labContent.content?.metadata?.[Globals.PREV_PUB_HASH]?.toString() ??
    '';

  return commitID;
}

/**
 * Checks if the lab content is empty.
 *
 * @param labContent The lab content to check.
 * @returns true if the lab content's cells are empty, false otherwise.
 */
function isBlankLab(labContent: ILabContent): boolean {
  if (typeof labContent === 'string') {
    try {
      labContent = JSON.parse(labContent);
    } catch (e) {
      console.error('Error parsing lab content string:', e);
      return false;
    }
  }

  if (
    typeof labContent !== 'object' ||
    labContent === null ||
    (!('cells' in labContent) &&
      !(labContent.content && 'cells' in labContent.content))
  ) {
    console.error(
      "Lab content is of unknown type or missing 'cells': ",
      typeof labContent,
      '\n Value: \n',
      labContent
    );
    return false;
  }

  const cells = (labContent as any).cells || (labContent as any).content?.cells;
  const isEmpty =
    cells.length === 0 || (cells.length === 1 && cells[0].source.length === 0);
  return isEmpty;
}

/**
 * Gets the raw data (cell models and content, notebook configurations) from the .ipynb file
 *
 * @param panel Notebook panel
 * @param context Notebook context
 */
export const getFileCellContentsOmitID = (
  panel: NotebookPanel,
  context: DocumentRegistry.IContext<INotebookModel>
): string => {
  const allCells: any[] = [];
  panel.content.widgets.forEach((cell: Cell<ICellModel>) => {
    const cellData = getCellContentsOmitID(cell);
    allCells.push(cellData);
  });

  return JSON.stringify(allCells, null, 2);
};

export const openIndependentLab = async (
  awb_token: string,
  docManager: IDocumentManager,
  contentsManager: Contents.IManager
): Promise<NotebookPanel> => {
  const { labFilename, body: instructions_content } =
    await getIndependentLabModel(awbAxiosHandler(awb_token), awb_token);

  let filePath = `${labFilename}`;

  if (ENV_TYPE !== EnvType.JUPYTERLITE) {
    // Outside of JupyterLite we want to use a relative path for some things
    filePath = `./${filePath}`;
    // We also want to delete the file if it is empty and create a backup if needed
    await deleteIfEmptyFile(filePath, contentsManager, docManager);
    await checkAndBackupSaveFile(
      filePath,
      instructions_content,
      contentsManager,
      docManager
    );
  } else {
    // Inside of JupyterLite we don't want persistent storage for authors, so we delete the existing file if it exists
    await docManager.deleteFile(filePath);
  }

  // Set the publish button to only show for the lab with title labFilename
  Globals.SHOW_PUBLISH_BUTTON_FOR = labFilename;
  // Set the publish button to only work for the lab with title labFilename
  Globals.TOKENS.set(labFilename, awb_token);

  const prevFile: Contents.IModel | null = await getFile(
    filePath,
    contentsManager
  );
  let nbPanel: NotebookPanel | undefined;
  if (!prevFile) {
    nbPanel = await createNotebook(
      docManager,
      labFilename,
      instructions_content
    );
  } else {
    nbPanel = docManager.openOrReveal(labFilename) as NotebookPanel;
  }

  return nbPanel;
};

export const openLab = async (
  token: string,
  docManager: IDocumentManager,
  contentsManager: Contents.IManager
): Promise<NotebookPanel> => {
  const { instructions_file_path, body: instructions_content } =
    await getLabModel(atlasAxiosHandler(token));

  const labFilename = getLabFileName(instructions_file_path);
  let filePath = `${labFilename}`;

  if (ENV_TYPE !== EnvType.JUPYTERLITE) {
    // Outside of JupyterLite we want to use a relative path for some things
    filePath = `./${filePath}`;
    // We also want to delete the file if it is empty and create a backup if needed
    await deleteIfEmptyFile(filePath, contentsManager, docManager);
    await checkAndBackupSaveFile(
      filePath,
      instructions_content,
      contentsManager,
      docManager
    );
  } else {
    // Inside of JupyterLite we don't want persistent storage for authors, so we delete the existing file if it exists
    await docManager.deleteFile(filePath);
  }

  // Set the publish button to only show for the lab with title labFilename
  Globals.SHOW_PUBLISH_BUTTON_FOR = labFilename;
  // Set the publish button to only work for the lab with title labFilename
  Globals.TOKENS.set(labFilename, token);

  const prevFile: Contents.IModel | null = await getFile(
    filePath,
    contentsManager
  );
  let nbPanel: NotebookPanel | undefined;
  if (!prevFile) {
    nbPanel = await createNotebook(
      docManager,
      labFilename,
      JSON.parse(instructions_content)
    );
  } else {
    nbPanel = docManager.openOrReveal(labFilename) as NotebookPanel;
  }

  return nbPanel;
};

export const openLearnerLab = async (
  notebookUrl: string,
  filePath: string | null,
  docManager: IDocumentManager,
  contentsManager: Contents.IManager,
  fileBrowser: IDefaultFileBrowser
): Promise<NotebookPanel> => {
  const response = await getLearnerLabModel(notebookUrl);

  const content: object | string = response.data;
  if (!isValidJson(content)) {
    throw Error(
      `content of ${notebookUrl} is not a valid JSON! Please let the author know about this issue!`
    );
  }

  const lastModifiedDateFromHeader = Date.parse(
    response.headers['last-modified'] || ''
  );
  console.log(
    `last-modified date of ${notebookUrl} extracted from headers:`,
    lastModifiedDateFromHeader
  );

  if (!filePath || !filePath.endsWith('.ipynb')) {
    console.log(
      `filePath from query (which is ${filePath}) is either missing or doesn't end with .ipynb. Trying to use the pathname from ${notebookUrl} as filePath...`
    );
    filePath = decodeURI(new URL(notebookUrl).pathname);
    if (!filePath.endsWith('.ipynb')) {
      throw Error(
        `pathname of ${notebookUrl} (which is ${filePath}) doesn't end with .ipynb. A notebook can't be created.`
      );
    }
  }

  console.log('filePath:', filePath);

  await ensureSubFoldersExist(docManager, filePath);

  console.log(`Opening ${filePath} in filebrowser`);
  await fileBrowser.model.cd(filePath.substring(0, filePath.lastIndexOf('/')));

  const prevFile: Contents.IModel | null = await getFile(
    filePath,
    contentsManager
  );
  let nbPanel: NotebookPanel | undefined;
  if (!prevFile) {
    console.log('Creating a new notebook');
    nbPanel = await createNotebook(docManager, filePath, content);
    return nbPanel;
  }

  console.log(
    'last-modified date of',
    filePath,
    'extracted from notebook:',
    Date.parse(prevFile.last_modified)
  );

  if (
    !lastModifiedDateFromHeader ||
    lastModifiedDateFromHeader > Date.parse(prevFile.last_modified)
  ) {
    const result = await showDialog({
      title: 'Newer version of notebook available',
      body: `A newer version of the lab is available. Would you like to load the latest version? The current state of the notebook ${filePath} will be saved with a .backup.ipynb extension.`,
      buttons: [
        Dialog.cancelButton(),
        Dialog.okButton({ label: 'Use the newer version' })
      ]
    });
    if (result.button.accept) {
      console.log('Opening newer version of notebook');
      await docManager.overwrite(
        filePath,
        filePath.slice(0, filePath.lastIndexOf('.ipynb')) + '.backup.ipynb'
      );
      nbPanel = await createNotebook(docManager, filePath, content);
    } else {
      console.log('Opening existing notebook');
      nbPanel = docManager.openOrReveal(filePath) as NotebookPanel;
    }
  } else {
    console.log('Opening existing notebook');
    nbPanel = docManager.openOrReveal(filePath) as NotebookPanel;
  }

  return nbPanel;
};

/**
 * Creates a new notebook panel with the given content
 *
 * @param docManager the JupyterLab document manager
 * @param filePath the path of the file
 * @param content the content of the notebook
 * @throws Error if the notebook panel can't be created
 * @returns the notebook panel
 */
export const createNotebook = async (
  docManager: IDocumentManager,
  filePath: string,
  content: any
) => {
  const nbPanel = docManager.createNew(filePath, 'notebook', {
    name: Globals.PY_KERNEL_NAME
  }) as NotebookPanel;
  if (nbPanel === undefined) {
    throw Error('Error loading lab');
  }
  await loadLabContents(
    nbPanel,
    content as unknown as nbformat.INotebookContent
  );
  return nbPanel;
};

/**
 * Checks if the system file with the same name is empty, if so delete it, else
 * renames the system file to filename.backup.ipynb, and overwrites the original filename.backup.ipynb
 *
 * @param {string} labFilename - Path to string.
 * @param {ILabContent} instructions_content - Lab instructions
 * @param {ContentsManager} contentsManager - The JupyterLab contents manager.
 * @returns {Promise<void>} - Returns nothing
 */
async function checkAndBackupSaveFile(
  labFilename: string,
  instructions_content: ILabContent,
  contentsManager: Contents.IManager,
  docManager: IDocumentManager
): Promise<void> {
  const prevFile: Contents.IModel | null = await getFile(
    labFilename,
    contentsManager
  );
  if (prevFile) {
    const currCommitID = getLabCommitID(instructions_content);
    const prevCommitID = getLabCommitID(prevFile);
    if (currCommitID !== prevCommitID) {
      try {
        await convertFileToBackup(prevFile, contentsManager, docManager);
        await showDialog({
          title: 'Your Lab was Updated',
          body: `The newest published version of "${labFilename}" is loaded. Your previous version has been backed up under "${labFilename}${Globals.BACKUP_EXT}.ipynb"`,
          buttons: [Dialog.okButton({ label: 'Dismiss' })]
        });
      } catch (e) {
        console.error('[checkAndBackupSaveFile] Error during file backup', e);
        await showDialog({
          title: 'Error with Previous File',
          body: `While trying to load your lab: "${labFilename}", we found that you have another file named "${labFilename}" that already exists in this folder, please delete it or rename it so we can load your published version"`,
          buttons: [Dialog.okButton({ label: 'Dismiss' })]
        });
      }
    }
  }
}

/**
 * Checks if the system file is empty, if so delete it.
 *
 * @param {string} labFilename - Path to string.
 * @param {ILabContent} instructions_content - Lab instructions
 * @param {ContentsManager} contentsManager - The JupyterLab contents manager.
 * @returns {Promise<void>} - Returns nothing
 */
async function deleteIfEmptyFile(
  labFilename: string,
  contentsManager: Contents.IManager,
  docManager: IDocumentManager
): Promise<void> {
  const file: Contents.IModel | null = await getFile(
    labFilename,
    contentsManager
  );
  if (file) {
    await closeWithoutSaving(labFilename, docManager);
    if (isBlankLab(file)) {
      await contentsManager.delete(labFilename);
    }
  }
}

export const loadLabContents = async (
  widget: NotebookPanel,
  notebook_content: nbformat.INotebookContent,
  author_env?: string
): Promise<void> => {
  // Wait for widget to initalize correctly before making changes
  await widget.context.ready;

  if (author_env !== 'local') {
    // Load content
    widget.context.model.fromJSON(notebook_content);
    // Save content
    try {
      // TODO: Minor Bug that can confuse user - after loading and saving,
      // user is still prompted to save because JLabs updates the saved ipynb's metadata
      await widget.context.save();
    } catch (error) {
      console.error('[loadLabContents] Error saving notebook:', error);
    }
  } else {
    console.error(
      '[loadLabContents] Notebook model is not initialized or authoring environment is local.'
    );
  }
};

export const getLabFileName = (lab_filepath: any): string => {
  const labFilePath = lab_filepath ?? Globals.DEFAULT_LAB_NAME;
  // Extract filename from filepath
  // TODO: This is required as the createNew method will not automatically create the parent directories
  return labFilePath.replace(/^.*[\\/]/, '');
};

/**
 * Renames a file to filename.backup.ipynb and overwrites any files with the same name.
 *
 * @param {string} path - path to string.
 * @param {ContentsManager} contentsManager - The JupyterLab contents manager.
 * @returns {Promise<IModel | null>} - Returns the file or null
 */
async function getFile(
  path: string,
  contentsManager: Contents.IManager
): Promise<Contents.IModel | null> {
  try {
    const file = await contentsManager.get(path);
    return file;
  } catch (error) {
    if (error instanceof Error) {
      const axiosError = error as AxiosError;

      if (axiosError.response && axiosError.response.status !== 404) {
        console.error('Error checking for existent backup file: ', error);
        throw error;
      } else {
        return null;
      }
    } else {
      console.error('[getFile] Unexpected error type:', error);
      throw error;
    }
  }
}

/**
 * Function that saves and close open widgets
 *
 * @param docManager - The JupyterLab document manager.
 * @param oldPath - The old path of the file.
 * @param newPath - The new path of the file.
 */
async function saveAndCloseOpenFiles(
  path: string,
  docManager: IDocumentManager
): Promise<void> {
  const widget = docManager.findWidget(path);
  if (widget) {
    try {
      if (widget.context.model.dirty) {
        await widget.context.save();
      }
      widget.close();
    } catch (error) {
      console.error(
        '[saveAndCloseOpenFiles] Error saving or closing widget:',
        error
      );
    }
  }
}

/**
 * Close the associated widget of a file without saving any changes.
 *
 * @param path - The path of the file.
 * @param docManager - The JupyterLab document manager.
 *
 */
async function closeWithoutSaving(
  path: string,
  docManager: IDocumentManager
): Promise<void> {
  const widget = docManager.findWidget(path);
  if (widget) {
    try {
      const context = docManager.contextForWidget(widget);
      if (context && context.model) {
        // Mark the context as not dirty to prevent the save prompt
        context.model.dirty = false;
      }
      widget.close();
    } catch (error) {
      console.error('[closeWithoutSaving] Error closing widget:', error);
    }
  }
}

/**
 * Takes a file and renames it filename.backup and overwrite any files with the same name
 *
 * @param {Contents.IModel} file - The file model to rename
 * @param {IContents.Manager} contentsManager - The JupyterLab contents manager.
 * @returns {Promise<void>} - returns after file is renamed
 */
async function convertFileToBackup(
  file: Contents.IModel,
  contentsManager: Contents.IManager,
  docManager: IDocumentManager
): Promise<void> {
  const prevPath = file.path;
  const fileExt = prevPath.split('.').pop();

  // removes the last portion of the string, separated by the last dot
  const fileNameWithoutExt = prevPath.replace(/\.[^/.]+$/, '');

  const newPath = `${fileNameWithoutExt}${Globals.BACKUP_EXT}.${fileExt}`;

  const prevFile = await getFile(newPath, contentsManager);

  if (prevFile) {
    try {
      await contentsManager.delete(newPath);
    } catch (error) {
      console.error(
        '[convertFileToBackup] Error deleting existing backup file:',
        error
      );
    }
  }

  try {
    // Saving and closing opened files to remove the sn-publish button
    await saveAndCloseOpenFiles(prevPath, docManager);
    await contentsManager.rename(prevPath, newPath);
  } catch (error) {
    console.error(
      '[convertFileToBackup] Error renaming file to backup:',
      error
    );
  }
}

export async function generateHash(data: string): Promise<string> {
  const encoder = new TextEncoder();
  const dataBuffer = encoder.encode(data);

  // Use the Web Crypto API to compute the SHA-256 hash of the binary data.
  const hashBuffer = await crypto.subtle.digest('SHA-256', dataBuffer);
  const hash = Array.from(new Uint8Array(hashBuffer))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
  return hash;
}

/**
 * Checks if the item is valid JSON
 *
 * @param item the item to check if it is valid JSON
 * @returns true if the item is a valid JSON, false otherwise
 */
export function isValidJson(item: object | string): boolean {
  item = typeof item !== 'string' ? JSON.stringify(item) : item;

  try {
    item = JSON.parse(item);
  } catch (e) {
    return false;
  }

  if (typeof item === 'object' && item !== null) {
    return true;
  }

  return false;
}

// eslint-disable-next-line @typescript-eslint/quotes
export const DEFAULT_CONTENT: nbformat.INotebookContent = {
  cells: [
    {
      cell_type: 'code',
      id: 'c852569f-bf26-4994-88e7-3b94874d3853',
      metadata: {},
      source: ['print("hello world again")']
    },
    {
      cell_type: 'markdown',
      id: '5a2dc856-763a-4f12-b675-481ed971178a',
      metadata: {},
      source: ['this is markdown']
    },
    {
      cell_type: 'raw',
      id: '492a02e8-ec75-49f7-8560-b30256bca6af',
      metadata: {},
      source: ['this is raw']
    }
  ],
  metadata: {
    kernelspec: {
      display_name: 'Python 3 (ipykernel)',
      language: 'python',
      name: 'python3'
    },
    language_info: {
      codemirror_mode: { name: 'ipython', version: 3 },
      file_extension: '.py',
      mimetype: 'text/x-python',
      name: 'python',
      nbconvert_exporter: 'python',
      pygments_lexer: 'ipython3',
      version: '3.10.4'
    }
  },
  nbformat: 4,
  nbformat_minor: 5
};

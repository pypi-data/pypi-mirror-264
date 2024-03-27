import { Widget } from '@lumino/widgets';
import { Dialog } from '@jupyterlab/apputils';
import { Globals, AWB_BASE_URL } from './config';
import jwt_decode from 'jwt-decode';

export class SkillsNetworkFileLibraryWidget extends Widget {

  constructor(contextPath: string) {

    function constructList(content: string, content_url: string) {
      const list = document.createElement('li');
      const link = document.createElement('a');
      link.textContent = content;
      link.style.color = "brown";
      link.href = content_url;
      link.style.textDecoration = "underline";
      link.style.cursor = "pointer";
      list.appendChild(link);

      return list;
    }

    const container = document.createElement('div');

    const subtitle = document.createElement('h2');
    subtitle.textContent = "File Library is not available for JupyterLab Classic.";
    container.appendChild(subtitle);

    const message = document.createElement('p');
    message.style.textAlign = "left";
    message.textContent = "Try opening the File Library from Author Workbench or upgrade your JupyterLab Classic to JupyterLab Current.";

    const List = document.createElement('ul');
    List.style.textAlign = "left";

    List.appendChild(constructList("How to access File Library from Author Workbench", "https://author.skills.network/docs/labs/jupyterlab-filelibrary"));
    List.appendChild(constructList("How to upgrade to JupyterLab Current", "https://author.skills.network/docs/labs/upgrade-jupyterlab"));

    container.appendChild(message);
    container.appendChild(List);
    container.style.padding = "20px";
    container.style.margin = "10px";
    container.style.textAlign = "center";

    super({ node: container });
  }
}

export class SkillsNetworkFileLibrary {
    #contextPath: string;

    constructor(contextPath: string) {
      this.#contextPath = contextPath;
    }

    launch(){
      const token = Globals.TOKENS.get(this.#contextPath.split('/').pop() || '');
      const token_info = token
      ? (jwt_decode(token) as { [key: string]: any })
      : {};
      const lab_content_url = AWB_BASE_URL + "/labs/" + token_info.lab_id + "?show=content";
      const imgLibDialog = new Dialog({title: "Skills Network File Library",
        body:  new SkillsNetworkFileLibraryWidget(lab_content_url),
        hasClose: true,
        buttons: [Dialog.cancelButton()]
      });
      const dialogContent = imgLibDialog.node.querySelector(".jp-Dialog-content")
      if (dialogContent){
        dialogContent.classList.add("sn-file-library-dialog");
      }
      imgLibDialog.launch()
    }
}

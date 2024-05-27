//画像を送って表示を消す処理
const form = document.getElementById("form")

const submitButton = document.getElementById("submit-button")

let parent = document.getElementById("list");


const progressBar = document.querySelector('.progress');
const progressBarText = progressBar.querySelector('.progress-bar');
submitButton.addEventListener('click', (e) => {
  e.preventDefault();
  var title = document.upload_form.title.value;
  if (title.length === 0) {
    alert('文字が入力されていません！');
    return false;
  }
  const xhr = new XMLHttpRequest();
  xhr.open('POST', 'https://localhost:5001/upload/'+user_name);
  xhr.upload.addEventListener('progress', (event) => {
      const percent = (event.loaded / event.total) * 100;
      progressBar.style.display = 'block';
      progressBarText.style.width = `${percent}%`;
      progressBarText.innerHTML = `${Math.round(percent)}%`;
  });
  //formのデータをすべて取得
  const formData = new FormData(form);
  const action = form.getAttribute("action")
  const options = {
    method: 'POST',
    body: formData,
  }
  //入力したデータを送る
  xhr.send(formData);
  xhr.onload = function () {
  if (xhr.status === 200 || xhr.status === 201) {
    progressBar.style.display = 'none';
    form.reset();
    while (parent.lastChild) {
      parent.removeChild(parent.lastChild);
    }
    alert('File uploaded successfully!');
  } else {
    alert('リクエストが失敗しました');
  }
};

});


// ファイルアップロードゾーン
const fileZone = document.querySelector('.file-zone');
// ファイルアップロードゾーンに着脱するクラス
const className = 'on';
// input[type=file]の取得/////////////////
const fileInput = document.getElementById('uploadFile');

// ドラッグした要素が重なったときの処理
fileZone.addEventListener('dragover', (event) => {
  // デフォルトの挙動を停止
  event.preventDefault();
  fileZone.classList.add(className);
});

// ドラッグした要素が離れたときの処理
fileZone.addEventListener('dragleave', (event) => {
  // デフォルトの挙動を停止
  event.preventDefault();
  fileZone.classList.remove(className);
});

// ドロップした時の処理
fileZone.addEventListener('drop', (event) => {
  // デフォルトの挙動を停止
  event.preventDefault();
  fileZone.classList.remove(className);
  // Fileオブジェクトを参照
  var filelist = event.dataTransfer.files;
  // ファイルにfilelistを入れる
  fileInput.files = filelist;
  displayImages(filelist);
});

// input[type=file]に変更があれば実行
// もちろんドロップ以外でも発火します
fileInput.addEventListener('change', (e) => {
  var filelist = e.target.files;
  if (typeof e.target.files !== 'undefined') {
    // ファイルが正常に受け取れた際の処理
    displayImages(filelist);
    alert("!!");
  } else {
    // ファイルが受け取れなかった際の処理
  }
}, false);

///ここから下が画像表示処理///
/** 画像の表示処理 */

function displayImages(filelist) {
  // 画像ファイルの格納配列
  const imageFileList = [];
  // ファイル数
  const fileNum = filelist.length;
  let parent = document.getElementById("list");

  // ファイルが画像のもののみを配列に格納する
  for (let i = 0; i < fileNum; i++) {
    if (i > 6) {
      alert("6枚以下にしてください");
      form.reset();
      while (parent.lastChild) {
        parent.removeChild(parent.lastChild);
      }
      return;
    }
    else {
      if (filelist[i].type.match('image.*') === false) {
        return;
      }
      imageFileList.push(filelist[i]);
    }
  }

  const imagePreviewArea = document.querySelector('.image-list');

  ///画像を切り替えるために削除
  while (parent.lastChild) {
    parent.removeChild(parent.lastChild);
  }

  // 各画像ファイルにlocalURLを生成
  for (const imageFile of imageFileList) {
    // 画像ファイルの読み込み処理
    const fileReader = new FileReader();
    fileReader.readAsDataURL(imageFile);
    fileReader.addEventListener('load', (event) => {
      const image = new Image();
      image.src = event.target.result;
      // 表示エリアの先頭に画像ファイルを表示
      imagePreviewArea.insertBefore(image, imagePreviewArea.firstChild);

    });
  }
}




///////////////////////
//動画を送って表示を消す処理
const video_form = document.getElementById("video_form")
const video_submitButton = document.getElementById("video-submit-button")
var video_preview = document.getElementById('v_list');

const progressBar_video = document.querySelector('.progress-video');
const progressBarText_video = progressBar_video.querySelector('.progress-bar-video');
video_submitButton.addEventListener('click', (e) => {
  e.preventDefault();
  var title = document.video_upload_form.title.value;
  if (title.length === 0) {
    alert('文字が入力されていません！');
    return false;
  }
  const xhr = new XMLHttpRequest();
  xhr.open('POST', 'https://localhost:5001/video_upload/'+user_name);
  xhr.upload.addEventListener('progress', (event) => {
      const percent = (event.loaded / event.total) * 100;
      progressBar_video.style.display = 'block';
      progressBarText_video.style.width = `${percent}%`;
      progressBarText_video.innerHTML = `${Math.round(percent)}%`;
  });
  //formのデータをすべて取得
  const formData = new FormData(video_form);
  const action = video_form.getAttribute("action")
  const options = {
    method: 'POST',
    body: formData,
  }
  //入力したデータを送る
  xhr.send(formData);
  xhr.onload = function () {
  if (xhr.status === 200 || xhr.status === 201) {
    progressBar_video.style.display = 'none';
    video_form.reset();
    while (video_preview.lastChild) {
      video_preview.removeChild(video_preview.lastChild);
    }
    alert("保存しました。")
  } else {
    alert('リクエストが失敗しました');
  }
};

});

/*
video_submitButton.onclick = () => {
  var title = document.video_upload_form.title.value;
  if (title.length === 0) {
    alert('文字が入力されていません！');
    return false;
  }
  const formData = new FormData(video_form)
  const action = video_form.getAttribute("action")
  const options = {
    method: 'POST',
    body: formData,
  }
  fetch(action, options).then((e) => {
    if (e.status === 200) {
      video_form.reset();
      while (video_preview.lastChild) {
        video_preview.removeChild(video_preview.lastChild);
      }
      alert("保存しました。")
      return
    }
    alert("保存できませんでした。")
  })
}*/

// ファイルアップロードゾーン
const v_fileZone = document.querySelector('.v_file-zone');
// ファイルアップロードゾーンに着脱するクラス
const v_className = 'v_on';
//ファイルプレビューエリア
var video_preview = document.getElementById('v_list');

// input[type=file]の取得/////////////////
var v_fileInput = document.getElementById('v_uploadFile');
// ドラッグした要素が重なったときの処理
v_fileZone.addEventListener('dragover', (event) => {
  // デフォルトの挙動を停止
  event.preventDefault();
  v_fileZone.classList.add(v_className);
});

// ドラッグした要素が離れたときの処理
v_fileZone.addEventListener('dragleave', (event) => {
  // デフォルトの挙動を停止
  event.preventDefault();
  v_fileZone.classList.remove(v_className);
});

// ドロップした時の処理
v_fileZone.addEventListener('drop', (event) => {
  // デフォルトの挙動を停止
  event.preventDefault();
  //変更があった時に、今表示されている動画を削除
  while (video_preview.lastChild) {
    video_preview.removeChild(video_preview.lastChild);
  }
  v_fileZone.classList.remove(v_className);
  // Fileオブジェクトを参照
  var v_filelist = event.dataTransfer.files;
  v_fileInput.files = v_filelist;
  // Blob URLの作成
  var blobUrl = window.URL.createObjectURL(v_filelist[0]);
  var video = document.createElement('video');
  video.src = blobUrl; // 動的に生成した動画のURL
  video.setAttribute("controls", "");
  video_preview.appendChild(video);
}
);

// input[type=file]に変更があれば実行
// もちろんドロップ以外でも発火します
v_fileInput.addEventListener('change', (e) => {
  var v_filelist = e.target.files;
  
  if (typeof e.target.files !== 'undefined') {
    // ファイルが正常に受け取れた際の処理
    // Blob URLの作成

    //変更があった時に、今表示されている動画を削除
    while (video_preview.lastChild) {
      video_preview.removeChild(video_preview.lastChild);
    }
    var blobUrl = window.URL.createObjectURL(v_filelist[0]);
    var video = document.createElement('video');
    video.src = blobUrl; // 動的に生成した動画のURL
    video.setAttribute("controls", "");
    video_preview.appendChild(video);
    alert("!!");
  } else {
    // ファイルが受け取れなかった際の処理
  }
}, false);


////////////////////
//オーディオ + 画像を送って表示を消す処理
const audio_form = document.getElementById("audio_form")
const audio_submitButton = document.getElementById("audio-submit-button")
let audio_parent = document.getElementById("audio_list");


const progressBar_audio = document.querySelector('.progress-audio');
const progressBarText_auido = progressBar_audio.querySelector('.progress-bar-audio');
audio_submitButton.addEventListener('click', (e) => {
  e.preventDefault();
  var title = document.audio_upload_form.title.value;
  if (title.length === 0) {
    alert('文字が入力されていません！');
    return false;
  }
  const xhr = new XMLHttpRequest();
  xhr.open('POST', 'https://localhost:5001/audio_upload/'+user_name);
  xhr.upload.addEventListener('progress', (event) => {
      const percent = (event.loaded / event.total) * 100;
      progressBar_audio.style.display = 'block';
      progressBarText_auido.style.width = `${percent}%`;
      progressBarText_auido.innerHTML = `${Math.round(percent)}%`;
  });
  //formのデータをすべて取得
  const formData = new FormData(audio_form);
  const action = audio_form.getAttribute("action")
  const options = {
    method: 'POST',
    body: formData,
  }
  //入力したデータを送る
  xhr.send(formData);
  xhr.onload = function () {
  if (xhr.status === 200 || xhr.status === 201) {
    progressBar_audio.style.display = 'none';
    audio_form.reset();
    while (audio_parent.lastChild) {
      audio_parent.removeChild(audio_parent.lastChild);
    }
    alert("保存しました。")
  } else {
    alert('リクエストが失敗しました');
  }
};

});

// ファイルアップロードゾーン
const audio_fileZone = document.querySelector('.audio_file-zone');
// ファイルアップロードゾーンに着脱するクラス
const audio_className = 'audio_on';
// input[type=file]の取得/////////////////
var audio_fileInput = document.getElementById('audio_uploadFile');
// ドラッグした要素が重なったときの処理
audio_fileZone.addEventListener('dragover', (event) => {
  // デフォルトの挙動を停止
  event.preventDefault();
  audio_fileZone.classList.add(audio_className);
});
// ドラッグした要素が離れたときの処理
audio_fileZone.addEventListener('dragleave', (event) => {
  // デフォルトの挙動を停止
  event.preventDefault();
  audio_fileZone.classList.remove(audio_className);
});

// ドロップした時の処理
audio_fileZone.addEventListener('drop', (event) => {
  // デフォルトの挙動を停止
  event.preventDefault();
  audio_fileZone.classList.remove(audio_className);
  // Fileオブジェクトを参照
  var audio_filelist = event.dataTransfer.files;
  audio_fileInput.files = audio_filelist;

  //画像を消すためのaudio_parent
  let audio_parent = document.getElementById("audio_list");
  while (audio_parent.lastChild) {
    audio_parent.removeChild(audio_parent.lastChild);
  }

  //アルバム画像の表示
  const audio_imagePreviewArea = document.querySelector('.audio-list');
  const audio_fileReader = new FileReader();
  audio_fileReader.readAsDataURL(audio_filelist[0]);
  audio_fileReader.addEventListener('load', (event) => {
  const audio_image = new Image();
  audio_image.src = event.target.result;
  // 表示エリアの先頭に画像ファイルを表示
  audio_imagePreviewArea.insertBefore(audio_image, audio_imagePreviewArea.firstChild);
  });
});

// input[type=file]に変更があれば実行
// もちろんドロップ以外でも発火します
audio_fileInput.addEventListener('change', (e) => {
  var audio_filelist = e.target.files;
  if (typeof e.target.files !== 'undefined') {
    // ファイルが正常に受け取れた際の処理

    //プレビューエリア
    const audio_imagePreviewArea = document.querySelector('.audio-list');
    
    //画像を消すためのaudio_parent
    let audio_parent = document.getElementById("audio_list");
    while (audio_parent.lastChild) {
      audio_parent.removeChild(audio_parent.lastChild);
    }
    const audio_fileReader = new FileReader();
    audio_fileReader.readAsDataURL(audio_filelist[0]);
    audio_fileReader.addEventListener('load', (event) => {
      const audio_image = new Image();
      audio_image.src = event.target.result;
      // 表示エリアの先頭に画像ファイルを表示
      audio_imagePreviewArea.insertBefore(audio_image, audio_imagePreviewArea.firstChild);
    });
    alert("!!");
  } else {
    // ファイルが受け取れなかった際の処理
  }
}, false);


////////////////////
//コードを表示するプログラム
const code_form = document.getElementById("code_form")
const code_submitButton = document.getElementById("code-submit-button")
let code_parent = document.getElementById("code_list");



const progressBar_code = document.querySelector('.progress-code');
const progressBarText_code = progressBar_code.querySelector('.progress-bar-code');
code_submitButton.addEventListener('click', (e) => {
  e.preventDefault();
  var title = document.code_upload_form.title.value;
  if (title.length === 0) {
    alert('文字が入力されていません！');
    return false;
  }
  const xhr = new XMLHttpRequest();
  xhr.open('POST', 'https://localhost:5001/code_upload/'+user_name);
  xhr.upload.addEventListener('progress', (event) => {
      const percent = (event.loaded / event.total) * 100;
      progressBar_code.style.display = 'block';
      progressBarText_code.style.width = `${percent}%`;
      progressBarText_code.innerHTML = `${Math.round(percent)}%`;
  });
  //formのデータをすべて取得
  const formData = new FormData(code_form);
  const action = code_form.getAttribute("action")
  const options = {
    method: 'POST',
    body: formData,
  }
  //入力したデータを送る
  xhr.send(formData);
  xhr.onload = function () {
  if (xhr.status === 200 || xhr.status === 201) {
    progressBar_code.style.display = 'none';
    code_form.reset();
    while (code_parent.lastChild) {
      code_parent.removeChild(code_parent.lastChild);
    }
    alert("保存しました。")
  } else {
    alert('リクエストが失敗しました');
  }
};

});

// ファイルアップロードゾーン
const code_fileZone = document.querySelector('.code_file-zone');
// ファイルアップロードゾーンに着脱するクラス
const code_className = 'code_on';
// input[type=file]の取得/////////////////
var code_fileInput = document.getElementById('code_uploadFile');

// ドラッグした要素が重なったときの処理
code_fileZone.addEventListener('dragover', (event) => {
  // デフォルトの挙動を停止
  event.preventDefault();
  code_fileZone.classList.add(code_className);
});

// ドラッグした要素が離れたときの処理
code_fileZone.addEventListener('dragleave', (event) => {
  // デフォルトの挙動を停止
  event.preventDefault();
  code_fileZone.classList.remove(code_className);
});

// ドロップした時の処理
code_fileZone.addEventListener('drop', (event) => {
  // デフォルトの挙動を停止
  event.preventDefault();
  code_fileZone.classList.remove(code_className);
  // Fileオブジェクトを参照
  var code_filelist = event.dataTransfer.files;
  code_fileInput.files = code_filelist;
});










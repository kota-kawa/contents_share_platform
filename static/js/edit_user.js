// input[type=file]の取得/////////////////
var background_fileInput = document.getElementById('input2');
var icon_fileInput = document.getElementById('input1');
////////////////////////
// input[type=file]に変更があれば実行
// もちろんドロップ以外でも発火します
background_fileInput.addEventListener('change', (e) => {
  var background_filelist = e.target.files;

  if (typeof e.target.files !== 'undefined') {
    // ファイルが正常に受け取れた際の処理
    background_displayImages(background_filelist);
    alert("!!");
  } else {
    // ファイルが受け取れなかった際の処理
  }
}, false);

///////////////////////
// input[type=file]に変更があれば実行
// もちろんドロップ以外でも発火します
icon_fileInput.addEventListener('change', (e) => {
  var icon_filelist = e.target.files;

  if (typeof e.target.files !== 'undefined') {
    // ファイルが正常に受け取れた際の処理
    icon_displayImages(icon_filelist);
    alert("!!");
  } else {
    // ファイルが受け取れなかった際の処理
  }
}, false);


////////////////////
function background_displayImages(background_filelist) {
  // 画像ファイルの格納配列
  const imageFileList = [];
  // ファイル数
  const fileNum = background_filelist.length;
  let parent = document.getElementById("imm");
  for (let i = 0; i < fileNum; i++) {
    while (parent.lastChild) {
      parent.removeChild(parent.lastChild);
    }
    if (background_filelist[i].type.match('image.*') === false) {
      return;
    }
    imageFileList.push(background_filelist[i]);
  }

  const imagePreviewArea = document.querySelector('.back_list');

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
function icon_displayImages(icon_filelist) {
  // 画像ファイルの格納配列
  const imageFileList = [];
  // ファイル数
  const fileNum = icon_filelist.length;
  let parent = document.getElementById("im");
  for (let i = 0; i < fileNum; i++) {
    while (parent.lastChild) {
      parent.removeChild(parent.lastChild);
    }
    if (icon_filelist[i].type.match('image.*') === false) {
      return;
    }
    imageFileList.push(icon_filelist[i]);
  }

  const imagePreviewArea = document.querySelector('.icon_list');

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

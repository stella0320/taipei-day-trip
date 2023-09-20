let generateImage = function(imageList) {
    console.log('image')
    const imageContainer = document.getElementById('imageContainer');
    const imageRadioContainer = document.getElementById('imageRadioContainer');
    for (let i=0 ;i < imageList.length ;i++) {
        let image = document.createElement('img');
        image.classList.add('main-content-section-image-image-img');
        image.src = imageList[i];
        imageContainer.appendChild(image);

        let radio = document.createElement('input');
        radio.type = 'radio';
        radio.classList.add('image-radio-item');
        radio.addEventListener('click', () => showImage(i+1));
        imageRadioContainer.appendChild(radio);
    }
    showImage();
}

let imageIndex = 1;

let showImage = function(imageNum) {
    if (imageNum) {
        imageIndex = imageNum;
    }
   
    let picList = document.getElementsByClassName('main-content-section-image-image-img');
    let radioList = document.getElementsByClassName('image-radio-item');
    for (let i = 0; i < picList.length; i++) {
        picList[i].style.display = "none";
        radioList[i].checked = false;
    }

    // 頁數超過照片數量，切回第一頁
    if (imageIndex > picList.length) {
        imageIndex = 1;
    }

    // 頁數小於0，切到最後一頁
    if (imageIndex <= 0) {
        imageIndex = picList.length;
    }

    radioList[imageIndex-1].checked = true;
    picList[imageIndex-1].style.display = "block";
}

function plusImage(n) {
    imageIndex += n;
    showImage();
}


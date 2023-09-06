
let appendAttrationCard = function(data) {

    const item = document.createElement('div');
    item.classList.add('index-main-content-attraction-item');

    const itemImage = document.createElement('div');
    itemImage.classList.add('index-main-content-attraction-image');

    // 圖片區域的圖片
    const itemImagePic = document.createElement('img');
    itemImagePic.classList.add('index-main-content-attraction-image-img');
    itemImagePic.src = data['image'][0];
    itemImage.appendChild(itemImagePic);

    // 圖片區域的文字
    const itemTitemImagePicTxt = document.createElement('div');
    itemTitemImagePicTxt.classList.add('index-main-content-attraction-image-txt');
    const itemTitemImagePicTxtText = document.createElement('div');
    itemTitemImagePicTxt.appendChild(itemTitemImagePicTxtText);
    const itemTitemImagePicTxtTextTxt = document.createTextNode(data['name']);
    itemTitemImagePicTxtText.appendChild(itemTitemImagePicTxtTextTxt);
    itemImage.appendChild(itemTitemImagePicTxt);
    
    // 下方文字區塊
    const itemText = document.createElement('div');
    itemText.classList.add('index-main-content-attraction-text');

    // Mrt
    const itemTextMrt = document.createElement('div');
    itemTextMrt.classList.add('index-main-content-attraction-text-mrt');
    const itemTextMrtText = document.createElement('div');
    itemTextMrt.appendChild(itemTextMrtText);
    const itemTextMrtTextTxt = document.createTextNode(data['mrt']);
    itemTextMrtText.appendChild(itemTextMrtTextTxt);

    // category
    const itemTextcategory = document.createElement('div');
    itemTextcategory.classList.add('index-main-content-attraction-text-category');
    const itemTextcategoryText = document.createElement('div');
    itemTextcategory.appendChild(itemTextcategoryText);
    const itemTextcategoryTextTxt = document.createTextNode(data['category']);
    itemTextcategoryText.appendChild(itemTextcategoryTextTxt);

    // itemText 塞Mrt&category
    itemText.appendChild(itemTextMrt);
    itemText.appendChild(itemTextcategory);

    // Item 塞圖片&文字
    item.appendChild(itemImage);
    item.appendChild(itemText);

    let container = document.getElementsByClassName('index-main-content-attraction-list')[0];
    container.appendChild(item);
}

let appendAttrationPage = function(data) {
    for (let i = 0; i < data.length; i++) {
        appendAttrationCard(data[i]);
    } 
}

let handleAttractionUrlResponse = async function (response) {
    
    if(response.status === 200){
        let result = await response.json();
        let data = result['data'];
        if (data && data.length > 0) {
            document.getElementById('attractionList').innerHTML = "";
            appendAttrationPage(data);
             // 置換nextPage
            let nextPage = document.getElementById('nextPage');
            nextPage.value = result['nextPage'];
        } else {
            document.getElementById('attractionList').innerHTML = "No Result.";
        }
       
    }else{
        console.log(response.status);
     // Rest of status codes (400,500,303), can be handled here appropriately
    }

}


let generateAttractions = function(page, keyword) {
    fetch('/api/attractions?page='+ page +'&keyword=' + encodeURIComponent(keyword))
    .then(handleAttractionUrlResponse)
    .catch((err) => {
        console.log(err);
    });
}


let initSearchBtn = function () {
    document.getElementById("searchBtn").addEventListener("click", function() {
        let keyword = document.getElementById("keyword").value;
        console.log('keyword:'+keyword);
        generateAttractions(0, keyword);
    });

}

let handleMrtUrlResponse = async function (response) {
    if(response.status === 200){
        let result = await response.json();
        let data = result['data'];

        // 建mrt清單
        console.log(data);
    }else{
        console.log(response.status);
     // Rest of status codes (400,500,303), can be handled here appropriately
    }
}

let generateMrtList = function () {
    fetch('/api/mrts')
    .then(handleMrtUrlResponse)
    .catch((err) => {
        console.log(err);
    });
}

generateMrtList();





initSearchBtn();
document.getElementById("searchBtn").click();
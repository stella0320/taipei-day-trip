
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

let pageList = [0];
let generateAttractions = function(page, keyword) {

    if (!(page + '')) {
        return;
    }
    
    if (pageList.indexOf(page) > -1) {
        return;
    }

    pageList.push(page);
    fetch('/api/attractions?page='+ page +'&keyword=' + encodeURIComponent(keyword))
    .then(handleAttractionUrlResponse)
    .catch((err) => {
        console.log(err);
    });
}


let initSearchBtn = function () {
    document.getElementById("searchBtn").addEventListener("click", function() {
        document.getElementById('attractionList').innerHTML = "";
        let keyword = document.getElementById("keyword").value;
        generateAttractions(0, keyword);
    });

}

let generateMrtLi = function (mrt) {
    const mrtLi = document.createElement('li');
    mrtLi.classList.add('index-main-content-mrt-list-item');
    const mrtLiTxt = document.createTextNode(mrt);
    mrtLi.appendChild(mrtLiTxt);
    let container = document.getElementById('allMrtList');
    container.appendChild(mrtLi);
}
let handleMrtUrlResponse = async function (response) {
    if(response.status === 200){
        let result = await response.json();
        let data = result['data'];
        for (let i = 0; i < data.length ; i++) {
            // 建mrt清單
            generateMrtLi(data[i]);
        }
    }else{
        console.log(response.status);
     // Rest of status codes (400,500,303), can be handled here appropriately
    }
}

let getMrtList = function () {
    fetch('/api/mrts')
    .then(handleMrtUrlResponse)
    .then(() => initMrtListClick())
    .catch((err) => {
        console.log(err);
    });
}

let initMrtListClick = function() {
    const mrtList = document.getElementsByClassName("index-main-content-mrt-list-item");
    for (let i = 0; i < mrtList.length ; i++) {
        let mrtLi = mrtList[i];
        mrtLi.addEventListener("click", function(event) {
            const value = event.target.innerHTML;
            document.getElementById("keyword").value = value;
            pageList = [];
            
            document.getElementById("searchBtn").click();
        });
    }
}

let initMrtBtn = function() {
    const container = document.querySelector('.index-main-content-mrt-list-container');
    const scrollList = document.querySelector('.index-main-content-mrt-list ul');
    const leftButton = document.getElementById('mrtLeftBtn');
    const rightButton = document.getElementById('mrtRightBtn');

    let scrollPosition = 0;

    leftButton.addEventListener('click', () => {
    scrollPosition -= 150 ; // 根据需要调整滚动的距离
    if (scrollPosition < 0) {
        scrollPosition = 0;
    }
    scrollList.style.transform = `translateX(${-scrollPosition}px)`;
    });

    rightButton.addEventListener('click', () => {
        scrollPosition += 150; // 根据需要调整滚动的距离
        const maxScroll = scrollList.scrollWidth - container.clientWidth;
        if (scrollPosition > maxScroll) {
            scrollPosition = maxScroll;
        }
        scrollList.style.transform = `translateX(${-scrollPosition}px)`;
    });
}

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        console.log('foot in');
        let keyword = document.getElementById("keyword").value;
        let nextPage = document.getElementById("nextPage").value;
        generateAttractions(nextPage, keyword);

      } else {
        // 目標元素離開 viewport 時執行
        console.log('foot out');
      }
    });
})

const footBox = document.getElementById('indexFoot');
observer.observe(footBox);

getMrtList();
initSearchBtn();
document.getElementById("searchBtn").click();
initMrtBtn();
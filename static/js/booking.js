let initBookingView = function(className) {
    const hideDivlist = document.querySelectorAll('div.booking-main-content:not(.booking-main-content-title, .no-booking-text)');
    for (let i=0;i < hideDivlist.length;i++) {
        hideDivlist[i].style.display = className;
    }
    
    const hrList = document.querySelectorAll('.booking-hr');
    for (let i=0;i < hrList.length;i++) {
        hrList[i].style.display = className;
    }

    const noBookingMessageClassName = className === 'none' ? 'block' : 'none';
    initnoBookingMessage(noBookingMessageClassName);
}

let initnoBookingMessage = function(className) {
    const noBookingMessage = document.querySelector('div.no-booking-text');
    noBookingMessage.style.display = className;
}

initBookingView('none');
initnoBookingMessage('none');

let dateFormat = function(dateStr) {
    const date = new Date(dateStr);
    const month = date.getMonth().toString().length == 1? ('0' + date.getMonth()) : date.getMonth();
    const day = date.getDate().toString().length == 1? '0' + date.getDate() : date.getDate();
    
    return date.getFullYear() + '-' + month + '-' + day;
}
let appendAttrationItem = function(appendElement, titileType, title, text) {
    const itemDiv = document.createElement('div');
    itemDiv.classList.add('booking-main-info-intro-item');

    const itemTitleDiv = document.createElement('div');
    itemTitleDiv.classList.add('booking-main-info-intro-title');
    itemTitleDiv.classList.add('font-text-style');

    const itemTitleText = document.createTextNode(title);
    itemTitleDiv.appendChild(itemTitleText);
    itemDiv.appendChild(itemTitleDiv);

    const itemTextDiv = document.createElement('div');
    itemTextDiv.classList.add('booking-main-info-intro-text');
    itemTextDiv.classList.add('font-text-style');
    if (titileType === 'time') {
        if (text === 'morning') {
            text = '早上九點到下午四點';
        } else if (text === 'afternoon') {
            text = '下午兩點到九點';
        }
    }
    
    if (titileType === 'date') {
        text = dateFormat(text);
    }

    if (titileType === 'price') {
        text = '新台幣' + text + '元';
    }
    const itemTextText = document.createTextNode(text);
    itemTextDiv.appendChild(itemTextText);
    itemDiv.appendChild(itemTextDiv);
    appendElement.appendChild(itemDiv);
}

let appendBookingAttractionElement = function(data) {
    
    const attraction = data['attraction'];
    
    const bookingInfoListDiv = document.getElementById('bookingInfoListDiv');
    const attractionItemDiv = document.createElement('div');
    attractionItemDiv.classList.add('booking-main-content');

    const attractionSubItemDiv = document.createElement('div');
    attractionSubItemDiv.classList.add('booking-sub-content');
    attractionSubItemDiv.classList.add('booking-main-info');
    

    const imageDiv = document.createElement('div');
    imageDiv.classList.add('booking-main-info-image');
    const image = document.createElement('img');
    image.classList.add('booking-main-info-image-img');
    const imageList = attraction['images'];

    if (imageList && imageList.length > 0) {
        image.src = imageList[0];
    }
    imageDiv.appendChild(image);
    attractionSubItemDiv.appendChild(imageDiv);

    const bookingIntroDiv = document.createElement('div');
    bookingIntroDiv.classList.add('booking-main-info-intro');
    

    const bookingIntroItemDiv = document.createElement('div');
    bookingIntroItemDiv.classList.add('booking-main-info-intro-item');
    bookingIntroItemDiv.classList.add('booking-main-info-intro-name');
    const bookingIntroItemTxt = document.createTextNode('台北一日遊：' + attraction['name']);
    bookingIntroItemDiv.appendChild(bookingIntroItemTxt);
    bookingIntroDiv.appendChild(bookingIntroItemDiv);
    attractionSubItemDiv.appendChild(bookingIntroDiv);

    appendAttrationItem(bookingIntroDiv, 'date', "日期：", data['date']);
    appendAttrationItem(bookingIntroDiv, 'time', "時間：", data['time']);
    appendAttrationItem(bookingIntroDiv, 'price', "費用：", data['price']);
    appendAttrationItem(bookingIntroDiv, null, "地點：", attraction['address']);

    const deleteItemDiv = document.createElement('div');
    deleteItemDiv.classList.add('booking-main-info-delete');

    const deleteImageImg= document.createElement('img');
    deleteImageImg.classList.add('booking-main-info-delete-btn');
    deleteImageImg.src = '/static/image/icon_delete.png';
    deleteImageImg.setAttribute('value', data['tripId']);
    deleteItemDiv.appendChild(deleteImageImg);
    attractionSubItemDiv.appendChild(deleteItemDiv);

    bookingInfoListDiv.appendChild(attractionItemDiv);
    attractionItemDiv.appendChild(attractionSubItemDiv);
}   

let queryBookingListEvent = async function(response) {    
    if (response.status == 200) {
        let result = await response.json();
        let data = result['data'];
        if (data.length > 0) {
            let totalPrice = 0;
            for (let i=0; i<data.length; i++) {
                let price = data[i]['price'];
                totalPrice += price;
                appendBookingAttractionElement(data[i]);
            }
            const totalPriceElement = document.getElementById('totalPrice');
            const totalPriceText = document.createTextNode('總價：新台幣 ' + totalPrice + ' 元');
            totalPriceElement.appendChild(totalPriceText);
            initBookingView('block');
        } else {
            initBookingView('none');
        }
        
    }
}

let queryBookingList = function() {
    const token = localStorage.getItem('token');
    fetch('/api/booking', {
        method: 'GET',
        headers: new Headers({
            Authorization: 'Bearer ' + token
        }) 
    })
    .then(queryBookingListEvent)
    .then(() => {
        let deleteBtnList = document.querySelectorAll('.booking-main-info-delete-btn');
        for (i=0; i< deleteBtnList.length; i++) {
            let deleteBtn = deleteBtnList[i];
            
            deleteBtn.addEventListener('click', function(e) {
                const tripId = e.target.getAttribute('value');
                if (tripId) {
                    fetch('/api/booking/' + tripId, {
                        method: 'DELETE',
                        headers: new Headers({
                            Authorization: 'Bearer ' + token
                        }) 
                    }).then((response) => {
                        if (response.status == 200) {
                            window.location = '/booking';
                        }
                    });
                }
            });
        }
    });
}

queryBookingList();


let initInputFormat = function() {
    const creditCard = document.getElementById('creditCard');


    creditCard.addEventListener('input', function (e) {
        console.log('input');
        let value = e.target.value.replace(/\s/g, ''); // 移除所有空格
        value = value.replace(/(.{4})\s/g, '$1 '); // 在每四個字符後插入一個空格
        console.log(value);
        e.target.value = value.trim(); // 移除可能的前導和尾隨空格
    });

}

// initInputFormat();

const token = localStorage.getItem('token');
if (!token) {
    window.location = '/';
}
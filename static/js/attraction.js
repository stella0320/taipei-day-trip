let fillUpAttrationInfo = function(data) {
    console.log('info')
    const attractionName = document.getElementById('attractionName');
    const attractionNameText = document.createTextNode(data['name']);
    attractionName.appendChild(attractionNameText);

    const attractionMrtAndCategory = document.getElementById('attractionMrtAndCategory');
    const attractionMrtAndCategoryText = document.createTextNode(data['category'] + ' at ' + data['mrt']);
    attractionMrtAndCategory.appendChild(attractionMrtAndCategoryText);

    const attractionDiscription = document.getElementById('attractionDiscription');
    const attractionDiscriptionText = document.createTextNode(data['description']);
    attractionDiscription.appendChild(attractionDiscriptionText);

    const attractionLocation = document.getElementById('attractionLocation');
    const attractionLocationText = document.createTextNode(data['address']);
    attractionLocation.appendChild(attractionLocationText);
    
    const attractionTransportation = document.getElementById('attractionTransportation');
    const attractionTransportationText = document.createTextNode(data['transport']);
    attractionTransportation.appendChild(attractionTransportationText);

    const bookingTripBtn = document.getElementById('bookingTripBtn');
    bookingTripBtn.setAttribute('value', data['id']);
    
}

let handleAttractionById = async function(response) {
    if(response.status === 200){
        let result = await response.json();
        if (result) {
            fillUpAttrationInfo(result['data']);
            generateImage(result['data']['images'])
        } else {
            window.location = '/';
            console.log('data not find');
        }
    }else{
        console.log(response.status);
        window.location = '/';
     // Rest of status codes (400,500,303), can be handled here appropriately
    }
}

let queryAttrationById = function () {
    const id = document.getElementById('attractionId').value;
    if (!id) {
        return;
    }
    fetch('../api/attraction/' + id)
    .then(handleAttractionById)
    .then(function() {
        // 資料載入後，show基本頁面
        console.log('visible');
        document.getElementById('content').style.visibility = "visible";
    })
    .catch((err) => {
        console.log(err);
    });
}


let iniTripTimeChange = function() {
    let tripTimeList = document.getElementsByName('tripTime');
    for (let i=0; i < tripTimeList.length;i++) {
        const item =  tripTimeList[i];
        item.addEventListener('click', function(event) {
            let tripTime = document.querySelector('input[name=tripTime]:checked').value;
            let tripFee = "";
            if (tripTime == "timeMorning") {
                tripFee = "新台幣2000元";
            } else if (tripTime == "timeEvening") {
                tripFee = "新台幣2500元";
            }
             
            if (tripFee) {
                let tripFeeDiv = document.getElementById('tripFee');
                tripFeeDiv.innerHTML = "";
                let tripFeeText = document.createTextNode(tripFee);
                tripFeeDiv.appendChild(tripFeeText);
            }
        });
    }

   
}



let bookingTripBtnEvent = function() {
    const id = document.getElementById('bookingTripBtn').getAttribute('value');
    const token = localStorage.getItem('token');
    const tripDate = document.getElementById('tripDate').value;
    const tripPeriod = document.querySelector('input[name=tripTime]:checked').value;
    fetch('/api/booking', {
        method:"POST",
        body:JSON.stringify({
            id: id,
            tripDate : tripDate,
            tripPeriod : tripPeriod
        }),
        headers: new Headers({
            "Content-Type": "application/json",
            "Authorization": 'Bearer ' + token
        })
    }).then((response) => {
        if (response.status == '200') {
            // 預定行程成功，導到booking頁面
            window.location = '/booking';
        } else {
            console.log(response.status);
        }
    });
}
let initBookingTripBtn = function() {
    document.getElementById('bookingTripBtn').addEventListener('click', bookingTripBtnEvent);
}

// 資料還沒載入時，先不顯示基本頁面
document.getElementById('content').style.visibility = "hidden";
// 載入景點訊息
queryAttrationById();
// 選擇時間change
iniTripTimeChange();
// 預定行程按鈕
initBookingTripBtn();
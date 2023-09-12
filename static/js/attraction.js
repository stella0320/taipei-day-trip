let fillUpAttrationInfo = function(data) {
    console.log(data);
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
    
}

let handleAttractionById = async function(response) {
    if(response.status === 200){
        let result = await response.json();
        if (result) {
            fillUpAttrationInfo(result['data']);
        } else {
            window.location = '/';
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
        document.getElementById('content').style.visibility = "visible";
    })
    .catch((err) => {
        console.log(err);
    });
}

// 資料還沒載入時，先不顯示基本頁面
document.getElementById('content').style.visibility = "hidden";
// 載入景點訊息
queryAttrationById();
// 選擇時間change
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

iniTripTimeChange();
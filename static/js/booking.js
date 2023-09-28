// userAuthWithToken


let initBookingIntroduction = async function(name) {
    // const name = document.getElementById('name').value;
    // console.log(document.getElementById('name'));
    const bookingIntroduction = document.getElementById('bookingIntroduction');

    const introText = document.createTextNode('您好，' + name + '，待預訂的行程如下');
    bookingIntroduction.appendChild(introText);
    // 在header.js執行
}


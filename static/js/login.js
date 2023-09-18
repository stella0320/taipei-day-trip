
let loginModeLinkEvent = function() {
    const loginTitle = document.getElementById('loginTitle');
    const loginBtn = document.getElementById('loginBtn');
    const loginName = document.getElementById('loginNameDiv');
    const loginModeLink = document.getElementById('loginModeLink');
    const loginBtnTxt = loginBtn.innerText;
    if (loginBtnTxt == "登入帳戶") {
        // 切換成註冊模式
        loginTitle.innerText = '註冊會員帳號';
        // login name
        loginName.style.display = 'block';
        // btn inner text
        loginBtn.innerText = '註冊新帳戶';
        // mode text
        loginModeLink.innerText = '已經有帳戶了？點此登入';
    } else {
        // 切換成登入模式
        loginTitle.innerText = '登入會員帳號';
        loginName.style.display = 'none';
        loginBtn.innerText = '登入帳戶';
        loginModeLink.innerText = '還沒有帳戶？點此註冊';
    }
}

let loginBtnEvent = function() {
    
    let formData = new FormData();
    const name = document.getElementById('loginName').value;
    const mail = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    formData.append("name", name);
    formData.append("mail", mail);
    formData.append("password", password);

    fetch('/api/user', {
        method:"POST",
        body: JSON.stringify({
            name:name,
            mail:mail,
            password:password
        }),
        headers: new Headers({
            "Content-Type": "application/json",
        })
    })
    .then((res) => {
        if (res.status == '400') {
            console.log('重複註冊');
        } else if (res.status == '200') {
            console.log('200');
        } else {
            console.log('500');
        }
        console.log(res.text());
    });
}

const loginModeLink = document.getElementById('loginModeLink');
loginModeLink.addEventListener('click', loginModeLinkEvent);

const loginBtn = document.getElementById('loginBtn');
loginBtn.addEventListener('click', loginBtnEvent);
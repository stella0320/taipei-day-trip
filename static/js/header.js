let initClickIndex = function() {
    document.getElementById('title').addEventListener('click', function() {
        window.location = '/';
    });
}

let deleteUserToken = function() {
    localStorage.removeItem('token');
    window.location = '/';
}

let initLoginBtn = function() {
    
    const headerLoginBtn = document.getElementById('headerLoginBtn');
    headerLoginBtn.addEventListener('click', function() {

        // 如果是登出，需要取消token
        if (headerLoginBtn.getAttribute('value') == 'logout') {
            deleteUserToken();
        } else {
            loginModal.style.display = 'block';
        }
    });
}


let userAuthorithation = function() {
    const token = localStorage.getItem('token');
    if (token) {
        fetch('/api/user/auth', {
            method:'GET',
            headers: new Headers({
                Authorization: 'Bearer ' + token
            })
        })
        .then(async function(res) {
            if (res.status == '400') {
                console.log('重複註冊');
            } else if (res.status == '200') {
                const response = await res.json();
                const user = response['data'];
                if (user) {
                    const loginModalDisplayStyle = loginModal.style.display;
                    if (loginModalDisplayStyle == 'block') {
                        loginModal.style.display = 'none';
                    }
                    const headerLoginBtn = document.getElementById('headerLoginBtn');
                    headerLoginBtn.innerText = user['name'] + '/登出系統';
                    headerLoginBtn.setAttribute('value', 'logout');

                    const name = document.getElementById('name');
                    name.setAttribute('value', user['name']);

                     
                    const bookingTitle = document.getElementById('bookingTitle');
                    // booking.html
                    if (bookingTitle) {
                        const introText = document.createTextNode('您好，' + user['name'] + '，待預訂的行程如下');
                        bookingTitle.appendChild(introText);
                    }
                }
            } else {
                console.log('500');
            }
        });
    }
    return token;
}

let initPreserveListBtn = function() {
    document.getElementById('preserveListBtn').addEventListener('click', function() {
        const token = userAuthorithation();
        if (!token) {
            loginModal.style.display = 'block';
        } else {
            // booking
            window.location = '/';
        }
    });
}

initClickIndex();
initLoginBtn();
initPreserveListBtn();
userAuthorithation();
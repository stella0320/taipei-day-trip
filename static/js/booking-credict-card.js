const appId = 137143;
const appKey = 'app_voc7R7iqSLwz6G317QB4Bl2QaYq6eFd3aRABDMMqoicm3nijQDX8JuxW5AES';
TPDirect.setupSDK(appId, appKey, 'sandbox');

let fields = {
    number : {
        element: '#creditCard',
        placeholder: '**** **** **** ****'
    },
    expirationDate: {
        element: '#expirationDate',
        placeholder: 'MM/YY'
    },
    ccv: {
        element: '#ccv',
        placeholder: 'CCV'
    }
}
TPDirect.card.setup({
   

    fields: fields,
    styles: {
        'input': {
            'color': 'gray'
        },
        ':focus': {
            'color': 'black'
        },
        // style valid state
        '.valid': {
            'color': 'green'
        },
        // style invalid state
        '.invalid': {
            'color': 'red'
        }
    }
})

function onSubmit(event) {
    event.preventDefault()

    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()

    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        alert('can not get prime')
        return
    }

    // Get prime
    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            alert('get prime error ' + result.msg)
            return
        }
        alert('get prime 成功，prime: ' + result.card.prime)

        // send prime to your server, to pay with Pay by Prime API .
        // Pay By Prime Docs: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-prime-api
    })
}
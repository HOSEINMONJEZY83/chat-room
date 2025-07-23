function checklogin() {
    const formData = $('#login-form').serialize();
    $.post('/', formData).then(res => {
            if(res.status ==='invalid input'){
                Swal.fire({
                icon: res.icon,
                title: res.status,
                text: res.text
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = '/';
    }
        })
            }else if(res.status ==="success"){
               Swal.fire({
                icon: res.icon,
                title: res.status,
                text: res.text
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = '/chatroom';
                    var border = document.getElementById('border');
                    border.scrollTop = border.scrollHeight;
    }
        })
            }
        }).catch(error => {
        Swal.fire({
            icon: 'error',
            title: 'wrong.',
            text: 'try again later...'
        }).then((result) => {
                if (result.isConfirmed) {
                    window.location.reload();
    }
        })
    });
    }


function checksignup() {
    const formData = $('#signup-form').serialize();
    $.post('/signup', formData).then(res => {
            if(res.status ==='invalid input'){
                Swal.fire({
                icon: res.icon,
                title: res.status,
                text: res.text
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = '/signup';
    }
        })
            }else if(res.status ==="success"){
               Swal.fire({
                icon: res.icon,
                title: res.status,
                text: res.text
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = '/chatroom';
                    var border = document.getElementById('border');
                    border.scrollTop = border.scrollHeight;
    }
        })
            }
        }).catch(error => {
        Swal.fire({
            icon: 'error',
            title: 'wrong.',
            text: 'try again later...'
        }).then((result) => {
                if (result.isConfirmed) {
                    window.location.reload();
    }
        })
    });
    }


function changeinformation() {
    const formData = new FormData($('#changeinformation')[0]);
    $.ajax({
        url: '/changeinformation',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
    }).then(res => {
        if (res.status === 'invalid input') {
            Swal.fire({
                icon: res.icon,
                title: res.status,
                text: res.text
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = '/changeinformation';
                }
            });
        } else if (res.status === "success") {
            Swal.fire({
                icon: res.icon,
                title: res.status,
                text: res.text
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = '/account';
                }
            });
        }
    }).catch(error => {
        Swal.fire({
            icon: 'error',
            title: 'wrong.',
            text: 'try again later...'
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.reload();
            }
        });
    });
}



function changepassword() {
    const formData = $('#changepassword').serialize();
    $.post('/changepassword', formData).then(res => {
            if(res.status ==='invalid input'){
                Swal.fire({
                icon: res.icon,
                title: res.status,
                text: res.text
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = '/changepassword';
    }
        })
            }else if(res.status ==="success"){
               Swal.fire({
                icon: res.icon,
                title: res.status,
                text: res.text
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = '/';
    }
        })
            }
        }).catch(error => {
        Swal.fire({
            icon: 'error',
            title: 'wrong.',
            text: 'try again later...'
        }).then((result) => {
                if (result.isConfirmed) {
                    window.location.reload();
    }
        })
    });
    }


function sendmessages() {
    var text = $('#messagetext').val();
    var fileInput = $('#messagefile')[0];
    var file = fileInput ? fileInput.files[0] : null;

    var formData = new FormData();
    formData.append('message', text);
    if (file) {
        formData.append('file', file);
    }

    const csrftoken = document.querySelector('[name=csrf-token]').content;

    $.ajax({
        url: '/sendmessage',
        type: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        data: formData,
        processData: false,
        contentType: false,
        success: function(res) {
            if (res.status === 'invalid input') {
                Swal.fire({
                    icon: res.icon,
                    title: res.status,
                    text: res.text
                }).then((result) => {
                    if (result.isConfirmed) {
                        var border = document.getElementById('border');
                        border.scrollTop = border.scrollHeight;
                    }
                });
            }
            else if (res) {
                $('#border').append(res);
                $('#messagetext').val('');
                $('#messagefile').val('');
                var border = document.getElementById('border');
                border.scrollTop = border.scrollHeight;
            }
        }
    });
}


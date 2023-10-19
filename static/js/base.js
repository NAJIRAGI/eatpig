// 모달 창 닫는 함수
$('.modal_close').click(function () {
    $('#first_modal').css({
        "display": "none"
    });
    $('#second_modal').css({
        "display": "none"
    });
    $('#third_modal').css({
        "display": "none"
    });
    $(document.body).css({
        "overflow": "scroll"
    });
    $('.modal_upload_space').css({
        "background-image": "none"
    });
});


$('#arrow_up').click(function (){
    $('html, body').animate({scrollTop: '0'}, 20);
});

// 전역 변수로 어디 서든 사용 가능 하도록
let files;

$('#content_add_box').click(function () {
    $('html, body').animate({scrollTop: '0'}, 20);

    $('#first_modal').css({
        "display": "flex"
    });

    $(document.body).css({
        "overflow": "hidden"
    });
});


$('#feed_create_btn').click(function () {

    const file = files[0];
    let img = files[0].name;
    let content = $('#input_feed_area').val();
    let select_menu = document.getElementById('menu');
    let menu = (select_menu.options[select_menu.selectedIndex].text);
    let select_region = document.getElementById('region');
    let region = (select_region.options[select_region.selectedIndex].text);
    let diner = $('#input_diner_name').val();

    // content가 공백인지 확인
    if (content.trim() === '') {
        alert("내용을 입력하세요");
        return; // 공백인 경우 함수 종료
    }


    let fd = new FormData();
    fd.append('file', file);
    fd.append('img', img);
    fd.append('content', content);
    fd.append('menu', menu)
    fd.append('region', region)
    fd.append('diner', diner)


    $.ajax({
        url: "/contents/upload",
        data: fd,
        method: "POST",
        processData: false,
        contentType: false,
        success: function (data) {
            console.log('업로드 성공');
        },
        error: function (request, status, error) {
            console.log('에러가 발생 했습니다.');
        },
        complete: function () {
            console.log('완료');
            location.replace('/contents/content_list')
        }
    });

});


$('#modal_upload')
    .on("dragover", dragOver)
    .on("dragleave", dragOver)
    .on("drop", uploadFiles);

function dragOver(e) {
    e.stopPropagation();
    e.preventDefault();

    if (e.type == "dragover") {
        $(e.target).css({
            "background-color": 'black',
            "outline-offset": '-20px'
        });

    } else {
        $(e.target).css({
            "background-color": 'gray',
            "outline-offset": '-10px'
        });
    }
}

function uploadFiles(e) {
    e.stopPropagation();
    e.preventDefault();

    e.dataTransfer = e.originalEvent.dataTransfer;
    files = e.target.files || e.dataTransfer.files;

    if (files.length > 1) {
        alert("파일은 하나만 업로드 가능 합니다, 제일 맛있는 사진을 올려 주세요!");
        return;
    }

    if (files[0].type.match(/image.*/)) {
        $('#first_modal').css({
            "display": "none"
        });
        $('#second_modal').css({
            "display": "flex"
        });
        $('.modal_upload_space').css({
            "background-image": "url(" + window.URL.createObjectURL(files[0]) + ")",
            "outline": "none",
            "background-size": "100%",
            "background-repeat": "no-repeat",
            "background-position": "center"
        });
    } else {
        alert("이미지 파일만 업로드 가능 합니다.");
        return;
    }
}

$('#feed_next_btn').click(function () {
    $('#first_modal').css({
        "display": "none"
    });
    $('#second_modal').css({
        "display": "none"
    });
    $('#third_modal').css({
        "display": "flex"
    });
});

$('.delete_feed').click(function () {
    let feed_id = $(this).data('feed-id');

    $.ajax({
        url: "/contents/content_delete",
        method: "POST",
        data: {
            "feed_id": feed_id,
        },
        success: function (data) {
            console.log("성공");
            location.reload();
        },
        error: function () {
            console.log('에러가 발생 했습니다.');
        },
        complete: function () {
            console.log('완료');

        }
    });
});
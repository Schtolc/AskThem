
function getComet(){
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1/listen/',
        cache: false,
        timeout: 25000,
        data: { cid: window.location.pathname.slice(10) }
    }).success(function(resp) {
        if (resp!="") {
            var newId = "cometAnswer_"+resp
            $('#cometMagic').append('<div id=\"' + newId + '\"></div>')
            $('#' + newId).load('http://127.0.0.1/single_answer?aid='+resp);
            console.log(resp)
        }
        getComet();
    }).error(function(err, textStatus) {
        console.log(err)
        if(textStatus != 'timeout'){
            setTimeout(getComet, 10000);
        } else {
            getComet()
        }
    });
}

setTimeout(function(){
    getComet()
}, 3000);



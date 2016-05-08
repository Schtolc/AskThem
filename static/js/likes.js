$('.like').click(function() {
                        var qid = $(this).data('qid');
                        var typ =  $(this).data('typ');
                        var csrftoken = Cookies.get('csrftoken');
                        $.ajax({
                            type: 'POST',
                            url: '/like',
                            data: {qid: qid, typ: typ, 'csrfmiddlewaretoken': csrftoken}
                        }).done(function(resp) {
                            var add_value = $('#down_'+resp.qid).prop('disabled') == $('#up_'+resp.qid).prop('disabled') ? 1 : 2
                            if (resp.like) {
                                $('#like_'+resp.qid).html(parseInt($('#like_'+resp.qid).text())+add_value)
                                $('#up_'+resp.qid).prop('disabled', true)
                                $('#down_'+resp.qid).prop('disabled', false)
                            } else {
                                $('#like_'+resp.qid).html(parseInt($('#like_'+resp.qid).text())-add_value)
                                $('#down_'+resp.qid).prop('disabled', true)
                                $('#up_'+resp.qid).prop('disabled', false)
                            }
                        }).fail(function(err) {
                            console.log(err);
                        });
                    });
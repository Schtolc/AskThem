$('.correct').click(function() {
                        var aid = $(this).data('aid');
                        var checked =$(this).prop("checked");
                        var csrftoken = Cookies.get('csrftoken');
                        $.ajax({
                            type: 'POST',
                            url: '/correct',
                            data: {aid: aid, checked: checked, 'csrfmiddlewaretoken': csrftoken}
                        }).done(function(resp) {
                            if (resp.correct) {
                                $('#correct_'+resp.aid).html("Correct!")
                            } else {
                                $('#correct_'+resp.aid).html("")
                            }
                        }).fail(function(err) {
                            console.log(err);
                        });
                    });
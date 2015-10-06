$('span[class^="like-button"]').click(function(){
    var obj = $(this);
    var msg_id = obj.attr('data-message-id');
    var action = obj.attr('data-action');
    $.get(action, {msg_id: msg_id}, function(data) {
        obj.html(data);
        obj.toggleClass('label-success label-default');
    });
});

$('a[class^="delete-button"]').click(function(){
    var obj = $(this);
    var msg_id = obj.attr('data-message-id');
    var action = obj.attr('data-action');
    $.get(action, {msg_id: msg_id}, function(data) {
        if (data == 'deleted')
        {
            $('#body-of-' + msg_id).remove();
        };
    });
});

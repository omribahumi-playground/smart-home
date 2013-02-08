var API_BASE_URL = "/api";

function refreshButtons(container)
{
    $.get(
        API_BASE_URL + "/status",
        null,
        function(data){
            for (var relay_id in data)
            {
                var button = container.find('button[data-relay-id=' + relay_id + ']');

                // create a button if one does not exist
                if (!button.length)
                {
                    button = $('<button />');
                    button.addClass('relay');
                    button.text(relay_id);
                    button.attr('data-relay-id', relay_id);
                    button.click(function(){
                        $.post(
                            API_BASE_URL + '/relay/' + $(this).attr('data-relay-id'),
                            'toggle',
                            function(){
                                refreshButtons(container);
                            }
                        );
                    });
                    container.append(button);
                }

                var relay_status = data[relay_id];
                if (relay_status)
                {
                    button.addClass('relay_on').removeClass('relay_off');
                }
                else
                {
                    button.addClass('relay_off').removeClass('relay_on');
                }
            }
        }
    );
}

$(document).ready(function(){
    refreshButtons($('#container'));
});

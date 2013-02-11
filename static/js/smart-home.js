var API_BASE_URL = "/api";

function attachEvents() {
    $('input').change(function() {
        console.log(this);
        $.post(
            API_BASE_URL + '/relay/' + $(this).attr('name'),
            'toggle',
            function(){}
        );
    });
}

function loadButton(container) {
    $.get(
        API_BASE_URL + "/status",
        null,
        function(data){
            var html = '';
            for (var relay_id in data){
                var relay_status = data[relay_id];
                html += '<li>';
                html += '<strong>'+relay_id+'</strong>';
                html += '<div class="relay">';
                html += '<input type="checkbox" id="r-'+relay_id+'" name="'+relay_id+'" '+(relay_status ? 'checked="checked"' : '')+'/>';
                html += '<div class="bg"></div>';
                html += '<label for="r-'+relay_id+'"><span>ON</span><span>OFF</span></label>';
                html += '</div>';
                html += '</li>';
            }
            container.append(html);
            attachEvents();
        }
    );
}

$(document).ready(function(){
    loadButton($('#settings'));
});

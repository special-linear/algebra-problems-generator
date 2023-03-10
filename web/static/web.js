$(document).ready(function() {

new_variant_row = $('#new-variant-row');
new_variant_input = new_variant_row.find('#new-variant');

new_variant_input.on('paste',function (e) {
    clipboardData = e.clipboardData || e.originalEvent.clipboardData || window.clipboardData;
    text = clipboardData.getData('text');
    variants = text.split('\n').map(s => s.trim());
    if (variants.length > 1) {
        variants.forEach(new_variant);
        setTimeout(() => new_variant_input.val([]), 0);
    }
});

new_variant_input.keypress(function (e) {
    if (e.which == 13) {
        variant_name = new_variant_input.val().trim();
        if (variant_name != "") {
            new_variant(variant_name);
            new_variant_input.val([]);
        }
        return false;
    }
});



new_problem_cell = $('#new-problem-cell');
new_problem_select = new_problem_cell.find('#new-problem');

function problem_delete(problem_name) {
    return function() {
        $(`td[data-problem="${problem_name}"]`).remove();
        $(`#new-problem [data-problem="${problem_name}"]`).prop('disabled', false);
        // new_variant_row.find('button.problem-all, button.problem-none').remove();
    }
}

function problem_change_all(problem_name, state) {
    return function() {
        $(`td.checkbox-cell[data-problem="${problem_name}"] input.problem-checkbox`).prop('checked', state);
    }
}

new_problem_select.change(function () {
    problem_name = new_problem_select.val()
    new_problem_cell.before(
        `<td class="problem-cell" data-problem="${problem_name}">
            <div class="problem-name">${problem_name}</div>
            <div class="problem-delete-button">&#10060;</div>
        </td>`
    );
    $('.variant-row .variant-row-last-cell').before(checkbox_cell_str(true, problem_name));
    new_variant_row.find('.variant-row-last-cell').before(`
        <td data-problem="${problem_name}">
            <button class="problem-all">A</button>
            <button class="problem-none">N</button>
        </td>
    `);
    $(`.problem-cell[data-problem="${problem_name}"] .problem-delete-button`).click(problem_delete(problem_name));
    new_variant_row.find(`td[data-problem="${problem_name}"] button.problem-all`).click(
        problem_change_all(problem_name, true)
    );
    new_variant_row.find(`td[data-problem="${problem_name}"] button.problem-none`).click(
        problem_change_all(problem_name, false)
    );
    new_problem_select.val(0);
    new_problem_select.find(`[data-problem="${problem_name}"]`).prop('disabled', true);
});

generator_updates = $('#generator-updates');
output_textarea = $('#generator-output');

generator_button = $('#generator-button')
generator_stop_button = $('#generator-stop-button')

generator_button.click(function() {
    generator_button.prop('disabled', true);
    generator_stop_button.prop('disabled', false);
    data = problems_json();
    data['request'] = 'generate';
    request_id = makeid(12);
    data['request_id'] = request_id;
    console.log(data);
    generator_socket = new WebSocket(`ws://${location.host}/generator`);
    generator_socket.onopen = function () {
        generator_socket.send(JSON.stringify(data));
        console.log('request sent');
        output_textarea.val('');
    };
    generator_socket.onmessage = function (event) {
        data = JSON.parse(event.data);
        message = data['message']
        switch (data['type']) {
            case 'output':
                output_textarea.val(message);
                generator_stop_button.off('click');
                generator_stop_button.prop('disabled', true);
                generator_button.prop('disabled', false);
                generator_socket.close();
                break;
            case 'update':
                generator_updates.text(message);
                break;
        }
    };
    generator_socket.onclose = function () {
        console.log('socket closed');
    }
    generator_stop_button.click(function () {
        generator_button.prop('disabled', false);
        generator_stop_button.prop('disabled', true);
        generator_socket.send(JSON.stringify({'request': 'stop'}));
    });
});

});


function problems_json() {
    problems = []
    $('.problem-cell').each(function () {
        problems.push($(this).data('problem'));
    });
    variants = {}
    $('.variant-row').each(function () {
        variant_name = $(this).find('.variant-name').text();
        variant_problems = []
        $(this).find('.problem-checkbox').each(function (i) {
            if ($(this).is(':checked')) {
                variant_problems.push(i);
            }
        });
        variants[variant_name] = variant_problems;
    });
    return {'problems': problems, 'variants': variants}
}

function getRndInteger(min, max) {
  return Math.floor(Math.random() * (max - min + 1) ) + min;
}

function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

function escapeHtml(unsafe) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
 }
function checkbox_cell_str(checked, problem_name) {
    return `<td class="checkbox-cell" data-problem="${problem_name}">
                <input type="checkbox" ${checked ? 'checked' : ''} class="problem-checkbox">
            </td>`
}

function variant_delete(variant_row) {
    return function() {
        variant_row.remove();
    };
}

function variant_change_all(variant_row, state) {
    return function () {
        variant_row.find('input.problem-checkbox').prop('checked', state);
    };
}

function new_variant(variant_name) {
    checkboxes_str = ''
    $('.problem-cell').each(function () {
        checkboxes_str += checkbox_cell_str(true, $(this).data('problem'));
    });
    $('#new-variant-row').before(
        `<tr class="variant-row" data-variant="current">
            <th class="variant-name-cell">
                <div class="variant-name">${escapeHtml(variant_name)}</div>
                <div class="variant-delete-button">&#10060;</div>
            </th>
            ${checkboxes_str}
            <td class="variant-row-last-cell">
                <button class="variant-all">A</button>
                <button class="variant-none">N</button>
            </td>
        </tr>`
    );
    current_variant_row = $('tr[data-variant="current"]')
    current_variant_row.find('.variant-delete-button').click(variant_delete(current_variant_row));
    current_variant_row.find('button.variant-all').click(variant_change_all(current_variant_row, true));
    current_variant_row.find('button.variant-none').click(variant_change_all(current_variant_row, false));
    current_variant_row.removeAttr('data-variant');
}





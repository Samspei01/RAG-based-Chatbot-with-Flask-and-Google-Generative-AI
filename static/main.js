// Function to get the current timestamp
function getCurrentTimestamp() {
    return new Date();
}

// Function to render messages on the chat screen
function renderMessageToScreen(args) {
    let displayDate = (args.time || getCurrentTimestamp()).toLocaleString('en-IN', {
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
    });
    let messagesContainer = $('.messages');

    let message = $(`
        <li class="message ${args.message_side}">
            <div class="avatar"></div>
            <div class="text_wrapper">
                <div class="text">${args.text}</div>
                <div class="timestamp">${displayDate}</div>
            </div>
        </li>
    `);

    messagesContainer.append(message);
    setTimeout(function () {
        message.addClass('appeared');
    }, 0);
    messagesContainer.animate({ scrollTop: messagesContainer.prop('scrollHeight') }, 300);
}

// Send a message when the 'Enter' key is pressed
$(document).ready(function() {
    $('#msg_input').keydown(function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            $('#send_button').click();
        }
    });
});

// Function to display user messages
function showUserMessage(message, datetime) {
    renderMessageToScreen({
        text: message,
        time: datetime,
        message_side: 'right',
    });
}

// Function to display chatbot messages
function showBotMessage(message, datetime) {
    renderMessageToScreen({
        text: message,
        time: datetime,
        message_side: 'left',
    });
}

// Send message to the chatbot
$('#send_button').on('click', function(e) {
    let userMessage = $('#msg_input').val();
    showUserMessage(userMessage);
    $('#msg_input').val('');

    // Send message to the Flask server
    $.ajax({
        url: '/send_message',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ message: userMessage }),
        success: function(response) {
            showBotMessage(response.response);
        },
        error: function() {
            showBotMessage('Error sending message. Please try again.');
        }
    });
});

// Upload PDF file
$('#upload_button').on('click', function(e) {
    let fileInput = $('#file_input')[0];
    if (fileInput.files.length === 0) {
        $('#upload_status').text('Please select a PDF file to upload.');
        return;
    }

    let formData = new FormData();
    formData.append('pdf', fileInput.files[0]);

    $.ajax({
        url: '/upload',
        method: 'POST',
        processData: false,
        contentType: false,
        data: formData,
        success: function(response) {
            $('#upload_status').text(response.message);
            $('#view_document').show(); // Show the view document link
            $('#view_document').attr('href', '/uploads/input.pdf'); // Set the link to the uploaded document
        },
        error: function(xhr) {
            $('#upload_status').text(xhr.responseJSON.error || 'File upload failed.');
            $('#view_document').hide(); // Hide the view document link if there's an error
        }
    });
});

// Set initial bot message
$(window).on('load', function() {
    showBotMessage('Hello there! Type in a message or upload a PDF.');
});

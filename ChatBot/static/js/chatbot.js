$(document).ready(function () {
  $("#sendBtn").click(function () {
    const message = $("#userInput").val().trim();
    if (!message) return;

    // Add user message
    const userBubble = `<div class="chat-bubble user">${message}</div>`;
    $("#chatBox").append(userBubble);
    $("#userInput").val("");

    // Animate scroll to the bottom
    $("#chatBox").stop().animate({ scrollTop: $("#chatBox")[0].scrollHeight }, 500);

    // Mock bot response
    const botBubble = `<div class="chat-bubble bot">Processing...</div>`;
    $("#chatBox").append(botBubble);

    // Animate scroll again after adding bot response
    $("#chatBox").stop().animate({ scrollTop: $("#chatBox")[0].scrollHeight }, 500);

    // Fetch response from Flask backend
    $.ajax({
      url: "/get_response",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({ message: message }),
      success: function (data) {
        $("#chatBox .bot:last").text(data.response);
        $("#chatBox").stop().animate({ scrollTop: $("#chatBox")[0].scrollHeight }, 500);
      },
      error: function () {
        $("#chatBox .bot:last").text("Error fetching response.");
      },
    });
  });

  // Allow pressing Enter to send a message
  $("#userInput").keypress(function (e) {
    if (e.which == 13) {
      $("#sendBtn").click();
    }
  });
});

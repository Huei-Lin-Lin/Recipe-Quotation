$(function () {
  var $btnPost = $("#btnPost");
  var $cuisine = $("#cuisine");
  var $headcount = $("#headcount");
  var $result = $("#result");

  $btnPost.off("click").on("click", function () {
    $result.empty();
    $result.append(
      "<div class='loading text-center'>爬蟲中<br/><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div>"
    );
    $.ajax({
      url: "/message",
      data: { cuisine: $cuisine.val(), headcount: $headcount.val() },
      type: "POST",
      success: function (data) {
        $result.empty();
        for (var k in data) {
          var body =
            '<table><thead class="text-center"><tr><th colspan="2">' +
            k +
            "</th></tr></thead>";
          for (var v in data[k]) {
            body += "<tbody><tr>";
            if (Object.keys(data[k]).length > 1) {
              body += "<td>" + v + "</td><td>" + data[k][v] + "</td></tr>";
            } else {
              body += '<td colspan="2">' + data[k][v] + "</td></tr>";
            }
            body += "</tr></tbody>";
          }
          body += "</table>";
          $result.append(body);
        }
      },
      error: function (xhr) {
        alert("Ajax request 發生錯誤");
        $result.empty();
      },
    });
  });
});

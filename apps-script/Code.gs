/**
 * Gerelt Solutions Studio — вэбсайтын формуудыг хүлээн авагч.
 *
 * Хийх зүйл:
 *   1. Google Sheet-д мөр нэмнэ
 *   2. Мэдэгдлийн имэйл илгээнэ
 *
 * Тохируулах заавар: ТОХИРУУЛГА.md
 */

// Мэдэгдэл хүлээн авах имэйл хаяг
var NOTIFY_EMAIL = 'gereltsolutions01@gmail.com';

// Мэдээлэл бичих хуудасны нэр
var SHEET_NAME = 'Хүсэлтүүд';

// Хүснэгтийн ID. Хоосон бол скрипт хавсаргасан хүснэгтэд бичнэ
// (Sheet дотроос Extensions → Apps Script гэж үүсгэсэн бол хоосон үлдээнэ).
var SHEET_ID = '';

var HEADERS = ['Огноо', 'Төрөл', 'Нэр', 'Утас', 'Имэйл', 'Үйлчилгээ', 'Төсөв', 'Мессеж'];

function doPost(e) {
  try {
    var data = {};
    if (e && e.postData && e.postData.contents) {
      data = JSON.parse(e.postData.contents);
    }

    var row = [
      new Date(),
      data.type || '',
      data.name || '',
      data.phone || '',
      data.email || '',
      data.service || '',
      data.budget || '',
      data.message || ''
    ];

    appendRow_(row);
    notify_(data);

    return json_({ ok: true });
  } catch (err) {
    // Алдааг хүснэгтэд үлдээхгүй ч имэйлээр мэдэгдэнэ
    try {
      MailApp.sendEmail(NOTIFY_EMAIL, 'Gerelt: формын алдаа', String(err));
    } catch (ignore) {}
    return json_({ ok: false, error: String(err) });
  }
}

// Хөтчөөс шууд нээж шалгахад ажиллаж байгаа эсэхийг харуулна
function doGet() {
  return json_({ ok: true, service: 'Gerelt Solutions form endpoint' });
}

function appendRow_(row) {
  var ss = SHEET_ID ? SpreadsheetApp.openById(SHEET_ID) : SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
  }
  if (sh.getLastRow() === 0) {
    sh.appendRow(HEADERS);
    sh.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
    sh.setFrozenRows(1);
  }
  sh.appendRow(row);
}

function notify_(data) {
  var subject = '🔔 ' + (data.type || 'Хүсэлт') + ' — ' + (data.name || 'нэргүй');
  var lines = [
    'Төрөл:      ' + (data.type || '-'),
    'Нэр:        ' + (data.name || '-'),
    'Утас:       ' + (data.phone || '-'),
    'Имэйл:      ' + (data.email || '-'),
    'Үйлчилгээ:  ' + (data.service || '-'),
    'Төсөв:      ' + (data.budget || '-'),
    '',
    'Мессеж:',
    (data.message || '-'),
    '',
    '— gerelt-solutuions.com'
  ];
  MailApp.sendEmail({
    to: NOTIFY_EMAIL,
    subject: subject,
    body: lines.join('\n'),
    replyTo: data.email || undefined
  });
}

function json_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

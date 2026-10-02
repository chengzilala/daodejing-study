// 主题切换：古卷黄（light）/ 墨色（ink）
(function () {
  var btns = document.querySelectorAll('.ddj-theme-btn');

  function applyTheme(t) {
    if (t === 'ink') document.body.classList.add('ddj-ink');
    else document.body.classList.remove('ddj-ink');
    btns.forEach(function (b) {
      b.classList.toggle('active', b.getAttribute('data-theme') === t);
    });
    try { localStorage.setItem('ddj-theme', t); } catch (e) {}
  }

  btns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      applyTheme(btn.getAttribute('data-theme'));
    });
  });

  // 分组 tab：全部 / 道篇 / 德篇
  var tabs = document.querySelectorAll('.ddj-tab');
  var cards = document.querySelectorAll('.ddj-card');
  if (tabs.length && cards.length) {
    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        tabs.forEach(function (x) { x.classList.remove('active'); });
        tab.classList.add('active');
        var g = tab.getAttribute('data-g');
        cards.forEach(function (c) {
          c.style.display = (g === 'all' || c.getAttribute('data-group') === g) ? '' : 'none';
        });
      });
    });
  }

  // 记住上次主题
  try {
    var saved = localStorage.getItem('ddj-theme');
    if (saved) applyTheme(saved);
  } catch (e) {}
})();

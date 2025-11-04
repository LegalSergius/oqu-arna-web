document.addEventListener("DOMContentLoaded", function() {
const countdownEl = document.getElementById("countdown");
const sentLink = document.getElementById("sent-link")
let remaining = 59; // 59 секунд

sentLink.style.display = 'none'

function updateTimer() {
    // мин, сек
  const minutes = Math.floor(remaining / 60);
  const seconds = remaining % 60;

    // форматируем с ведущим нулём
  const mm = minutes < 10 ? "0" + minutes : minutes;
  const ss = seconds < 10 ? "0" + seconds : seconds;
    // отображаем
  countdownEl.textContent = mm + ":" + ss;

  if (remaining > 0) {
    remaining--;
  } else {
    clearInterval(timerId);
    // По окончании таймера выводим сообщение:
    countdownEl.textContent = "Можно отправить код снова!";
    sentLink.style.display = 'flex'
  }
}

  // Запускаем отсчёт
  const timerId = setInterval(updateTimer, 1000);
  // Вызываем сразу, чтобы не ждать 1 секунду до первого обновления
  updateTimer();
});





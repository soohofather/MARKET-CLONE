<script>
  let hour = new Date().getHours();
  let min = new Date().getMinutes();

  setInterval(() => (min = min + 1), 1000);
</script>

<header>
  <div class="info-bar__time">{hour}:{min}</div>
</header>
<main>
  <a class="write-btn" href="#/write">+ 글쓰기</a>
</main>
<footer></footer>

<style>
  .info-bar__time {
    color: blue;
  }
</style>

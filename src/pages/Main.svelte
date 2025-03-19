<script>
  import { onMount } from "svelte";
  import Footer from "../components/Footer.svelte";
  import { getDatabase, ref, onValue } from "firebase/database";

  const calcTime = (timestamp) => {
    const curTime = new Date().getTime();
    const time = new Date(curTime - timestamp - 9 * 60 * 60 * 1000);
    const hour = time.getHours();
    const minute = time.getMinutes();
    const second = time.getSeconds();

    if (hour > 0) return `${hour}시간 전`;
    else if (minute > 0) return `${minute}분 전`;
    else if (second > 0) return `${second}초 전`;
    else return "방금 막";
  };

  let hour = new Date().getHours();
  let min = new Date().getMinutes();

  $: items = [];

  const db = getDatabase();
  const itemsRef = ref(db, "items/");

  onMount(() => {
    onValue(itemsRef, (snapshot) => {
      const data = snapshot.val();
      items = Object.values(data).reverse();
    });
  });
</script>

<header>
  <div class="info-bar__time">{hour}:{min}</div>
</header>
<main>
  {#each items as item}
    <div class="item-list">
      <div class="item-list__img">
        <img src={item.imgUrl} alt={item.title} />
      </div>
      <div class="item-list__info">
        <div class="item-list__info-title">{item.title}</div>
        <div class="item-list__info-meta">
          {item.place}
          {calcTime(item.insertAt)}
        </div>
        <div class="item-list__info-price">{item.price}</div>
        <div class="item-list__info-description">{item.description}</div>
      </div>
    </div>
  {/each}
  <a class="write-btn" href="#/write">+ 글쓰기</a>
</main>
<Footer location={"home"} />

<style>
  .info-bar__time {
    color: blue;
  }
</style>

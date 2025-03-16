<script>
  import { onMount } from "svelte";
  import Footer from "../components/Footer.svelte";
  import { getDatabase, ref, onValue } from "firebase/database";

  let hour = new Date().getHours();
  let min = new Date().getMinutes();

  $: items = [];

  const db = getDatabase();
  const itemsRef = ref(db, "items/");

  onMount(() => {
    onValue(itemsRef, (snapshot) => {
      const data = snapshot.val();
      items = Object.values(data);
    });
  })
</script>

<header>
  <div class="info-bar__time">{hour}:{min}</div>
</header>
<main>
  {#each items as item}
  <div class="item-list">
    <div class = "item-list__img"></div>
    <div class="item-list__info">
      <div class="item-list__info-title">{item.title}</div>
      <div class="item-list__info-meta">{item.place}</div>
      <div class="item-list__info-price">{item.price}</div>
      <div class="item-list__info-description">{item.description}</div>
    </div>
  </div>
  {/each}
  <a class="write-btn" href="#/write">+ 글쓰기</a>
</main>
<Footer location={'home'} />

<style>
  .info-bar__time {
    color: blue;
  }
</style>

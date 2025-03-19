<script>
  import { onMount } from "svelte";
  import { getDatabase, ref, set, onValue } from "firebase/database";

  // Firebase Realtime Database 참조
  const db = getDatabase();

  // 현재 접속한 유저의 ID (랜덤 생성)
  const userId = `user_${Math.floor(Math.random() * 10000)}`;
  const userRef = ref(db, `characters/${userId}`);

  // 초기 위치 설정
  let character = { x: 5, y: 5 };
  set(userRef, character);

  // 키보드 이동 이벤트 핸들러
  const handleKeydown = (e) => {
    switch (e.key) {
      case "ArrowUp":
        character.y -= 1;
        break;
      case "ArrowDown":
        character.y += 1;
        break;
      case "ArrowLeft":
        character.x -= 1;
        break;
      case "ArrowRight":
        character.x += 1;
        break;
    }
    set(userRef, character); // Firebase에 업데이트
  };

  // 모든 플레이어들의 위치 가져오기
  let players = {};

  onMount(() => {
    // 키 이벤트 리스너 추가
    window.addEventListener("keydown", handleKeydown);

    // Firebase에서 실시간으로 데이터 수신
    const allPlayersRef = ref(db, "characters");
    onValue(allPlayersRef, (snapshot) => {
      players = snapshot.val() || {};
    });

    return () => {
      window.removeEventListener("keydown", handleKeydown);
    };
  });
</script>

<main>
  <h1>3주차_신입연수원_DAY5_팀장님 지시 업무_문제①</h1>
  <h5>
    이번에 간단한 사내 사이드 프로젝트로 게더타운과 비슷한 앱을 만들어보려 해요.
    결과물을 통해 정식 프로젝트가 될 가능성도 있어서 빠르게 결과물을 보여주고
    검증해야하는 상황이에요. 그렇기 때문에 백엔드를 구성하기보단 파이어베이스의
    RealtimeDB를 이용해서 자신만의 개성있는 게더타운을 만들어서 POC를
    구현해주세요! (배포까지 할 필요는 없음. 로컬에서 확인할 수 있으면 됨)
    (명심해주세요! 1차목표는 캐릭터의 움직임과 이를 실시간으로 다른
    클라이언트에서 확인할 수 있도록 업데이트하는 로직이에요! 1차 목표가 완료되면
    HTML과 CSS를 조작해서 개성 있는 컨셉을 만들어보세요~!) TIP : 1) 캐릭터의
    위치를 업데이트하려면, 먼저 파이어베이스 RealtimeDB 공식 문서를 먼저
    살펴보길 바래요! onValue라는 메서드를 써서 데이터베이스의 업데이트 사항을
    클라이언트에 즉각 반영할 수 있어요. 또한 내 캐릭터의 움직임을 서버에 set을
    통해 업데이트하면 되겠죠? 2) 캐릭터의 움직임을 구현하려면 캐릭터가 움직이는
    상태일 때를 감지해서, 스프라이트 이미지의 특정 부분을 애니메이션으로
    보여주면 돼요. 이해가 잘 안된다구요? 스프라이트 이미지에 대해 먼저
    공부해보고 움직임을 어떻게 적용할지 알아봐요~!
  </h5>
  <div class="game-container">
    {#each Object.entries(players) as [id, pos]}
      <div
        class="player"
        style="
            left: {pos.x * 40}px;
            top: {pos.y * 40}px;
            background-color: {id === userId ? 'blue' : 'red'};
          "
      ></div>
    {/each}
  </div>
</main>

<style>
  .game-container {
    position: relative;
    width: 400px;
    height: 400px;
    border: 2px solid black;
    background: lightgray;
  }

  .player {
    width: 40px;
    height: 40px;
    position: absolute;
    border-radius: 50%;
  }
</style>

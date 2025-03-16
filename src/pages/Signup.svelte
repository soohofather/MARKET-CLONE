<script
  src="https://cdnjs.cloudflare.com/ajax/libs/js-sha256/0.9.0/sha256.min.js"
>
  import Footer from "../components/Footer.svelte";

</script>

<form id="signup-form">
  <div>회원 가입</div>
  <div>
    <label for="id">아이디</label>
    <input type="text" id="id" name="id" required />
  </div>
  <div>
    <label for="password">비밀번호</label>
    <input type="password" id="password" name="password" required />
  </div>
  <div>
    <label for="password2">비밀번호 확인</label>
    <input type="password" id="password2" name="password2" required />
  </div>
  <div>
    <label for="name">이름</label>
    <input type="text" id="name" name="name" required />
  </div>
  <div>
    <label for="email">이메일</label>
    <input type="email" id="email" name="email" required />
  </div>
  <div>
    <button type="submit">회원가입</button>
  </div>
  <div id="password-info"></div>
</form>
<Footer />
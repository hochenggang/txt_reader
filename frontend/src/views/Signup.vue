<template>
  <div class="f-c">
    <Loading v-if="loading"/>
    <div class="form b">
      <p class="c h3">注册</p>
      <p v-if="error" class="c errmsg">{{errmsg}}</p>
      <input v-model="mail" class="b m" type="text" placeholder="邮箱">
      <input v-model="password" class="b m" type="password" placeholder="密码">
      <input v-model="password2" class="b m" type="password" placeholder="重复密码">
      <input v-on:click="login" class="b m point" type="submit" value="注册">
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Loading from "@/components/Loading.vue";

export default {
  name: "login",
  components: {
    Loading
  },
  data: function() {
    return {
      mail: "",
      password: "",
      password2: "",
      loading: false,
      error:false,
      errmsg:""
    };
  },
  mounted: function(){
    let user_id = localStorage["txt_reader_user_id"];
    let user_key = localStorage["txt_reader_user_key"];
    if (user_id || user_key){
      // console.log("已登录，尝试跳转。")
      location.assign("/#/all");
    }
  },
  methods: {
    login: function() {
      this.loading = true;
      let formData = new FormData();
      if (this.mail.length < 1){
        this.error = true;
        this.errmsg = "请填写邮箱地址";
        this.loading = false;
        return false
      }
      if (this.password.length < 1){
        this.error = true;
        this.errmsg = "请填写密码";
        this.loading = false;
        return false
      }
      if (this.password2.length < 1){
        this.error = true;
        this.errmsg = "请填写密码";
        this.loading = false;
        return false
      }
      if (this.password != this.password2){
        this.error = true;
        this.errmsg = "两次密码不一致";
        this.loading = false;
        return false
      }
      formData.append("m", this.mail);
      formData.append("p1", this.password);
      formData.append("p2", this.password2);

      axios
        .post("/api/user/new", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(() => {
          location.assign("/");
          alert("注册成功！")
        })
        .catch(error => {
          this.errmsg = error.response.data.body;
          this.error = true;
        })
        .finally(()=>{
          this.loading = false;
        });
    }
  }
};
</script>

<style>
.f-c {
  display: flex;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  justify-content: center;
  align-items: center;
}
.form {
  width: 20rem;
  padding: 1rem;
}

.b {
  border: 1px solid #1a2a3a;
}
.m {
  margin-top: 0.25rem;
}
.c {
  text-align: center;
}
.h3 {
  font-size: 1.25rem;
  font-weight: bold;
}
.point {
  cursor: pointer;
}
.errmsg {
  color: #ee3f4d;
}
</style>


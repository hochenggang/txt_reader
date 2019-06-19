<template>
  <div class="f-c">
    <Loading v-if="loading"/>
    <div class="form b">
      <p class="c h3">上传</p>
      <p v-if="error" class="c errmsg">{{errmsg}}</p>
      <input type="file" ref="file">
      
      <input v-on:click="upload" class="b m point" type="submit" value="上传">
    </div>
  </div>

</template>

<script>
import axios from "axios";
import Loading from "@/components/Loading.vue";

export default {
  name: "upload",
  components: {
    Loading
  },
  data: function() {
    return {
      file: "",
      loading: false,
      error: false,
      errmsg: ""
    };
  },
  mounted: function() {},
  methods: {
    upload: function() {
      this.file = this.$refs.file.files[0];
      console.log(this.file);
      if (!this.file){
        this.error = true;
        this.errmsg = "请先选择文件"
        return false
      }
      if (this.file.type != "text/plain"){
        this.error = true;
        this.errmsg = "抱歉，只接受 txt 文件"
        return false
      }
      this.loading = true;
      let formData = new FormData();
      formData.append('file', this.file);
      axios
          .post("/api/book/upload", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
              "x-user-id":localStorage["txt_reader_user_id"],
              "x-user-key":localStorage["txt_reader_user_key"],
            }
          })
          .then(() => {
            location.assign("/#/all");
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


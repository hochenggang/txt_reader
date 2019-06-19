<template>
  <!-- 阅读器 -->
  <div class="reader">
    <!-- <div class="leading">
        <div class="read-area">
            <p>阅读区域，上下翻动</p>
        </div>
        <div class="control-area">
            <p>控制区域，点击唤起</p>
        </div>
    </div>-->
    <!-- 等待图标 -->
    <Loading v-if="loading"/>

    <!-- 目录 -->
    <ReaderCatalogue v-if="now.show_catalogue" :now="now"/>
    <!-- 文本容器 -->
    <div
      class="text"
      v-if="now.chapter"
      ref="text"
      v-on:click="show_control = !show_control"
      v-html="'<p>' + this.now.catalog[this.now.index][1] + '</p>' + this.now.chapter"
    ></div>

    <!-- 控制器 -->
    <ul v-if="show_control" class="control">
      <!-- 第一列 -->
      <li>
        <span v-on:click="now.index--,show_control = !show_control">
          <svg
            role="img"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            aria-labelledby="circleArrowLeftIconTitle"
          >
            <path d="M10.5 15l-3-3 3-3"></path>
            <path d="M16.5 12H9"></path>
            <path stroke-linecap="round" d="M7.5 12H9"></path>
            <circle cx="12" cy="12" r="10"></circle>
          </svg>
        </span>
        <span v-on:click="now.show_catalogue = !now.show_catalogue,show_control = !show_control">
          <svg
            role="img"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            aria-labelledby="listIconTitle"
          >
            <path d="M10 7L18 7M10 12L18 12M10 17L18 17"></path>
            <line x1="7" y1="7" x2="7" y2="7"></line>
            <line x1="7" y1="12" x2="7" y2="12"></line>
            <line x1="7" y1="17" x2="7" y2="17"></line>
          </svg>
        </span>
        <span v-on:click="now.index++,show_control = !show_control">
          <svg
            role="img"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            aria-labelledby="circleArrowRightIconTitle"
          >
            <path d="M13.5 9l3 3-3 3"></path>
            <path d="M7.5 12H15"></path>
            <path stroke-linecap="round" d="M16.5 12H15"></path>
            <circle cx="12" cy="12" r="10"></circle>
          </svg>
        </span>
      </li>
    </ul>
  </div>
</template>

<script>
// 通过路由接收书籍ID
// 检查阅读记录，设置索引
// 书籍ID -> 请求目录
// 根据索引加载章节

import axios from "axios";
import Loading from "@/components/Loading.vue";
import ReaderCatalogue from "@/components/Reader-catalogue.vue";

export default {
  name: "reader",
  components: {
    Loading,
    ReaderCatalogue
  },
  data: function() {
    return {
      now: {
        id: "",
        index: 0,
        catalog: "",
        chapter: "",
        show_catalogue: false
      },
      show_control: false,
      loading: false
    };
  },
  directives: {
    // 设置此指令后，每次加载都会将该元素的滚动器移动到顶部
    scollTop: {
      update: function(el) {
        el.scrollTop = 0;
      }
    }
  },

  mounted: function() {
    // 获取通过路由传入的书籍ID
    this.now.id = this.$route.query.id;
    console.log(this.now.id);

    if (!localStorage[this.now.id]) {
      localStorage[this.now.id] = 0;
    }
    this.now.index = localStorage[this.now.id];

    // 请求目录数据
    this.load_catalog(this.now.id);
  },
  methods: {
    load_catalog: function(book_id) {
      this.loading = true;
      // 加载目录
      axios
        .get("/api/book/catalogue/" + book_id, {
          headers: {
            "x-user-id": localStorage["txt_reader_user_id"],
            "x-user-key": localStorage["txt_reader_user_key"]
          }
        })
        .then(response => {
          this.now.catalog = response.data;
          this.load_chapter();
        })
        .catch(() => {
          alert("加载目录失败");
        })
        .finally(() => {
          this.loading = false;
        });
    },

    load_chapter: function() {
      axios
        .get("/api/book/chapter/" + this.now.id + "/" + this.now.index, {
          headers: {
            "x-user-id": localStorage["txt_reader_user_id"],
            "x-user-key": localStorage["txt_reader_user_key"]
          }
        })
        .then(response => {
          this.now.chapter =
            "<p>" +
            response.data[1]
              .replace(/\n\n/g, "\n")
              .replace(/\n/g, "</p><p>")
              .replace(/\s/g, "") +
            "</p>";
        })
        .then(() => {
          // 设置标题
          document.title = this.now.catalog[this.now.index][1];
          // 保存进度
          localStorage[this.now.id] = this.now.index;
        });
    }
  },
  watch: {
    "now.index": function() {
      // 检测章节数据
      if (!this.now.catalog) {
        return false;
      }
      console.log("索引变化，即将加载需要的章节");
      if (this.now.index < 0) {
        this.now.index = 0;
        alert("已经是开头了！");
        return false;
      } else if (this.now.index >= this.now.catalog.length) {
        this.now.index = this.now.catalog.length - 1;
        alert("读完了喔！");
        return false;
      }
      this.load_chapter();
      this.$refs.text.scrollTop = 0;
    }
  }
};
</script>

<style>
.text {
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #f7f4ed;
  /* rgba(250, 235, 215, 0.6) */
  -webkit-overflow-scrolling: touch;
  padding: 0.5rem;
  overflow-y: auto;
}

.text p {
  text-indent: 2rem;
  line-height: 2rem;
  word-wrap: break-word;
  font-family: inherit;
  font-size: 1.1rem;
}

.control {
  position: fixed;
  bottom: 0;
  width: 100%;
  height: 3rem;
  background-color: #f7f4ed;
  z-index: 2;
  padding: 0.5rem;
}
.control > li {
  height: 2rem;
  display: flex;
  justify-content: space-around;
  align-items: center;
}
.control span {
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>

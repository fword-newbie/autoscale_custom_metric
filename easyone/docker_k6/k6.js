import http from "k6/http";
import { check, sleep } from "k6";

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min;
}

var r1 = getRandomInt(4, 20);

export const options = {
  thresholds: {
    http_req_duration: ["p(99) < 6000"],
  },
  stages: [
    { duration: "30s", target: r1 },
    { duration: "1m", target: r1 },
    { duration: "20s", target: r1 },
    { duration: "30s", target: r1 },
    { duration: "1m", target: r1 },
    { duration: "20s", target: r1 },
    { duration: "20s", target: r1 },
    { duration: "30s", target: r1 },
    { duration: "1m", target: r1 },
    { duration: "20s", target: r1 },
    { duration: "30s", target: r1 },
    { duration: "1m", target: r1 },
    { duration: "20s", target: r1 },
    { duration: "20s", target: r1 },
    { duration: "40s", target: r1 },
    { duration: "50s", target: r1 },
    { duration: "30s", target: r1 },
  ],
};

export default function () {
  let res = http.post("http://puyuan:8000/api/shock");
  // let res = http.get("http://httpcpuwaste-n:31112/adam");
  check(res, { "status was 200": (r) => r.status == 200 });
  sleep(1);
}

// export default function () {

//   var url = 'http://puyuan-s:5000/api/shock';
  
//   const params = {
//   headers: {
//     'Content-Type':'application/json',
//     'Accept':'application/json' 
//   },
//   timeout: 200,
//   };
  
//   let data = { name: 'jojo' };

//   let res = http.post(url,data,params);
//   console.log(res.body);
  
//   // Verify response 
//   check(res, {
//   'status is 200': (r) => r.status === 200
//   });
//   }
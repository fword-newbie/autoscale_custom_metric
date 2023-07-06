import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  thresholds: {
    http_req_duration: ["p(99) < 3000"],
  },
  stages: [
    { duration: "30s", target: 15 },
    { duration: "1m", target: 15 },
    { duration: "20s", target: 0 },
  ],
};

export default function () {
  let res = http.get("http://puyuan:8000/api/shock");
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
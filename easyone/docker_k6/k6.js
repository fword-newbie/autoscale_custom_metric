import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  thresholds: {
    http_req_duration: ["p(99) < 500"],
  },
  stages: [
    { duration: "1m", target: 40 },
    { duration: "1m", target: 40 },
    { duration: "1m", target: 40 },
    { duration: "1m", target: 40 },
    { duration: "1m", target: 40 },
    { duration: "1m", target: 40 },
    { duration: "1m", target: 40 },
    { duration: "1m", target: 40 },
    { duration: "1m", target: 40 },
    { duration: "1m", target: 40 },
  ],
};

export default function () {
  let res = http.post("http://puyuan:8000/api/shock");
  check(res, { "status was 200": (r) => r.status == 200 });
  sleep(1);
}

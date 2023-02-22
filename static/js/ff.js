

const currentTime = document.getElementById("time")

const now = new Date().getTime()
console.log(now)

let today = new Date()

const myCountDown = setInterval(()=>{
    let h = today.getHours()
    let m = today.getMinutes()
    let s = today.getSeconds()

    let tt = h + ":" + m + ":" + s
    s = s + 1
    console.log(tt)
}, 1000)
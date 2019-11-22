<template>
    <div class="container p-1">
        <div class="row">
            <div class="col">
                <div>Time left to proceed: <span 
                :class="['font-weight-bold', 'back-color', {
                    'back-color-1': selectedTime && endTime === 0 
                }]">{{ timeLeft }}</span>
                <span  v-if="is_expired">waiting for the payment</span> </div>
            </div>
            <div class="col col-md-6">
                <div class="switch text-switch text-right">
                    <div class="rate switch-item ">
                        1 LTCT <span style="color: #376097"><i class="fa fa-exchange"></i>
                        </span> 1,000.00 USD
                    </div>
                </div>
            </div>
        </div>
        
        <a-progress :percent="percent" :showInfo="false" strokeLinecap="square" 
        status="exception" :strokeColor="'#376097'" :successPercent="0"/>
    </div>
</template>

<script>
    var intervalTimer;

    export default {
        name: 'count-down',
        props: {
            count_down: Number,
            expired: Boolean,
        },
        data() {
            return {
                selectedTime: 0,
                timeLeft: '00:00',
                endTime: '0',
                percent: 100,
            }
        },
        computed:{
            is_expired() {
                return this.timeLeft != '00:00';
            },
            get_percentage(){
                return this.expired? this.percent : 100;
            }
        },
        methods: {
            setTime(seconds) {
                clearInterval(intervalTimer);
                this.timer(seconds);
            },
            timer(seconds) {
                const now = Date.now();
                const end = now + seconds * 1000;
                this.displayTimeLeft(seconds);

                this.selectedTime = seconds;

                this.displayEndTime(end);
                this.countdown(end);
            },
            countdown(end) {

                intervalTimer = setInterval(() => {
                    const secondsLeft = Math.round((end - Date.now()) / 1000);

                    if(secondsLeft === 0) {
                        this.endTime = 0;
                    }

                    if(secondsLeft < 0) {
                        clearInterval(intervalTimer);
                        return;
                    }
                    this.percent = 100 - ((this.selectedTime-secondsLeft) / this.selectedTime) * 100;
                    this.displayTimeLeft(secondsLeft)
                }, 1000);
            },
            displayTimeLeft(secondsLeft) {
                const minutes = Math.floor((secondsLeft % 3600) / 60);
                const seconds = secondsLeft % 60;
                this.timeLeft = `${zeroPadded(minutes)}:${zeroPadded(seconds)}`;
            },
            displayEndTime(timestamp) {
                const end = new Date(timestamp);
                const hour = end.getHours();
                const minutes = end.getMinutes();

                this.endTime = `${hourConvert(hour)}:${zeroPadded(minutes)}`
            },
        },
        mounted:function(){
            if(!this.expired){
                this.setTime(this.count_down)
            }
        }
    }

    function zeroPadded(num) {
        // 4 --> 04
        return num < 10 ? `0${num}` : num;
    }

    function hourConvert(hour) {
        // 15 --> 3
        return (hour % 12) || 12;
    }
</script>

<style lang="scss">
.ant-progress-inner {
  position: relative;
  display: inline-block;
  width: 100%;
  vertical-align: middle;
  background-color: #d1cdcd;
  border-radius: 0px;
  overflow: hidden;
}
.switch {
    color: #848484;
    font-size: 15px;
    font-weight: bold;

    .switch-item {
        display: inline-block;
        border-bottom: 1px dashed #acacac;
    }
    .text-switch {
        cursor: pointer;
    }
    fa{
        color: #39649d;
    }
}


</style>


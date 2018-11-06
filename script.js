let interval = 10000 ;
                    let chartinterval = 10*60000;
                    
                    
                    
                    
                    function startTime() {
                        let today = new Date();
                        let h = today.getHours();
                        let m = today.getMinutes();
                        let s = today.getSeconds();
                        let M = today.getMonth()+1;
                        let D = today.getDate();
                        let Y = today.getFullYear();
                        
                        m = checkTime(m);
                        s = checkTime(s);
                        document.getElementById('time').innerHTML =
                        `${D}.${M}.${Y} ${h}:${m}`
                        let t = setTimeout(startTime, 1000);
                    }
                    function checkTime(i) {
                        if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
                        return i;
                    }
                    
                    startTime()
                    
                    function fade(indexname){
                        indexname.classList.add = 'active'
                    }
                    
                    let myIndex = 0;
                    const repeat = chartinterval / interval;
                    let repeated = 0;
                    function slideShow() {
                        restart = 1;
                        x = document.getElementsByClassName('slides');
                            for (i = 0; i < x.length; i++){
                            x[i].style.display = 'none';
                            x[myIndex].classList.remove("active");
                            x[myIndex].style.display = 'inline-block';
                            }
                        setTimeout(function() {
                            x[myIndex].classList.add('active');
                            myIndex++;
                            repeated++;
                            if(repeated >= repeat && (myIndex+1) == x.length){
                                setTimeout(location.reload(true),interval - 2000)
                            }
                            if (myIndex == x.length) { myIndex = 0; }
                        },interval-2000);
                        setTimeout(slideShow, interval);
                    }
                    slideShow();
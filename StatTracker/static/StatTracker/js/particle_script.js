window.onload = function(){

    var canvas = document.getElementById("canvas");
    var ctx = canvas.getContext("2d");
    //Make the canvas occupy the full page
    var W = window.innerWidth, H = window.innerHeight;
    canvas.width = W;
    canvas.height = H;
    var particles = [];
    var decayingScaleFactor = 1;
    //Lets create some particles now
    var particle_count = 10;
    var spawnInterval = 2000;
    var i=0;
    var radiusDecayFactor = 0;
    var particlesSpawned = 0;
    function delayedParticleCreation(){
        setTimeout(function(){
            particles.push(new particle());
            i++;
            if (i < particle_count){
                delayedParticleCreation();
            }
            if (spawnInterval > 100){
                spawnInterval -= 100;
            }
        },spawnInterval)
    }
    delayedParticleCreation();

    function particle()
    {
        //speed, life, location, life, colors
        //speed.x range = -2.5 to 2.5
        //speed.y range = -15 to -5 to make it move upwards
        //lets change the Y speed to make it look like a flame
        var mirrorImageGenerator = Math.random();
        //radius range = 10-30
        this.radius = 1+Math.random()*9;
        //life range = 20-30
        this.life = 10000+Math.random()*10000;
        this.remainingLife = this.life;
        //colors
        nonGreenColorConstant = 50+Math.round(Math.random()*50);
        this.r = 50;
        this.g = 200+Math.round(Math.random()*55);
        this.b = nonGreenColorConstant+Math.round(Math.random()*155);
        if (mirrorImageGenerator >= 0.50) {
            this.geneticFlag = 1;
            this.location = {x: (W*0.5)+(20*Math.round(1-Math.random()*2)), y: (H*0.99)};
            this.speed = {x: 0, y: -17};
            }
        else {
            this.geneticFlag = 2;
            this.location = {x: (W*0.5)+320+(20*Math.round(1-Math.random()*2)), y: (H*0.99)};
            this.speed = {x: 0, y: -17};
            }
    }

    function draw()
    {;
        //Painting the canvas black
        //Time for lighting magic
        //particles are painted with "lighter"
        //In the next frame the background is painted normally without blending to the
        //previous frame
        ctx.globalCompositeOperation = "source-atop";
        ctx.fillStyle = "rgba(0,0,0,0.01)";
        ctx.fillRect(0, 0, W, H);
        ctx.globalCompositeOperation = "lighter";

        for(var i = 0; i < particles.length; i++)
        {
            var p = particles[i];

            //*****Progress Mark*****
            ctx.beginPath();
            //changing opacity according to the life.
            //opacity goes to 0 at the end of life of a particle
            p.opacity = Math.round(p.remainingLife/p.life*100)/100
            //a gradient instead of white fill
            var gradient = ctx.createRadialGradient(p.location.x, p.location.y, 0, p.location.x, p.location.y, p.radius);
            gradient.addColorStop(0, "rgba("+p.r+", "+p.g+", "+p.b+", "+p.opacity+")");
            gradient.addColorStop(0.5, "rgba("+p.r+", "+p.g+", "+p.b+", "+p.opacity+")");
            gradient.addColorStop(1, "rgba("+p.r+", "+p.g+", "+p.b+", 0)");
            ctx.fillStyle = gradient;
            ctx.arc(p.location.x, p.location.y, p.radius, Math.PI*2, false);
            ctx.fill();

            //lets move the particles
            p.remainingLife--;
            p.speed.x += 0.150;
            if (p.geneticFlag == 1) {
                p.location.x += decayingScaleFactor*(24*Math.sin(p.speed.x));
            }
            else {
                p.location.x += decayingScaleFactor*(-24*Math.sin(p.speed.x));
            }
            p.location.y += 1.0*p.speed.y;
            p.radius -= (radiusDecayFactor);
            //if (radiusDecayFactor > 0.005) {
            //    radiusDecayFactor *= 0.8;
            //   }
            //regenerate particles
            //if (particlesSpawned < 50){
                if(p.remainingLife < 0 || p.radius < 0 || p.location.y < 0 || p.location.y > H || p.location.x < 0 || p.location.x > W)
                {
                    //a brand new particle replacing the dead one
                    particles[i] = new particle();
                    particlesSpawned ++;
                }
            //}
        }
    }
    setInterval(draw, 32);
}
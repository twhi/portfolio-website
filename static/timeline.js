function VerticalTimeline( element ) {
   this.element = element;
   this.blocks = this.element.getElementsByClassName("cd-timeline__block");
   this.images = this.element.getElementsByClassName("cd-timeline__img");
   this.contents = this.element.getElementsByClassName("cd-timeline__content");
   // ..
};

VerticalTimeline.prototype.showBlocks = function() {
   var self = this;
   for( var i = 0; i < this.blocks.length; i++) {
      (function(i){
         if( self.contents[i].classList.contains("cd-timeline__content--hidden") && self.blocks[i].getBoundingClientRect().top <= window.innerHeight*self.offset ) {
            // add bounce-in animation
            self.images[i].classList.add("cd-timeline__img--bounce-in");
            self.contents[i].classList.add("cd-timeline__content--bounce-in");
            self.images[i].classList.remove("cd-timeline__img--hidden");
            self.contents[i].classList.remove("cd-timeline__content--hidden");
         }
      })(i);
   }
};
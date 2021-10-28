class Structure {
    /**
     * Builds a structure object given required paramaters or defaults.
     * @param  {String} divName   String that matches the div name in the index html file.
     * @param  {Object} dimensions (Optional) Dimension object that has been initialized.
     */
    constructor(divName, dimensions){
      this.divName = divName;
      this.dimensions;
      if(dimensions === undefined){
          this.dimensions = new Dimension();
      } else {
          this.dimensions = dimensions;
      }
      this.svg;
      this.add_svg_structure();
    }
  
    /**
     * Adds the svg structure to the main div.
     */
    add_svg_structure (){
      const wrapper = d3.select(this.divName);
      const svg = wrapper
          .append('svg')
            .attr('width', this.dimensions.width)
            .attr('height', this.dimensions.height)
          .append('g')
            .style('transform', `translate(${this.dimensions.margin.left}px, ${this.dimensions.margin.top}px)`);
  
      this.svg = svg;
    }
  
  }
class Dimension {
    /**
     * Builds a dimension object given required paramaters or defaults.
     * @param  {number} width
     * @param  {number} height
     * @param  {Object} margin  Object containing top, right, bottom, left numbers.
     */
    constructor(width, height, margin={top: 50, right: 50, bottom: 50, left: 50}){
      const window_min = d3.min([window.innerWidth, window.innerHeight]) * 0.90
      this.width = width || window_min;
      this.height = height || window_min;
      this.margin = margin;
    }
  
    /**
     * Getter method for the bounded width (width less margins).
     * @returns {number}
     */
    get boundedWidth(){
      return (this.width - this.margin.left - this.margin.right);
    }
  
    /**
     * Getter method for the bounded height (height less margins).
     * @returns {number}
     */
    get boundedHeight(){
      return (this.height - this.margin.top - this.margin.bottom);
    }
  }
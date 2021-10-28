async function drawChart(text_init_header, text_lines, text_final_header, text_lines_after, reverse=false) {

    // Build structure object given html selector and dimensions (Optional parameter)
    const custom_dimension = new Dimension(1200, 400);
    const structure = new Structure('#wrapper', custom_dimension);
    
    // Add all lines and setup transitions
    for (var line_inst in text_lines){

        // Add headers
        const initial_text_header_object = structure.svg
            .append('text')
            .attr('x', 0)
            .attr('y', 70 * line_inst - 2)
            .attr('fill','#ebeed7')
            .style('font-size', '1.0em')
            .text(text_init_header);
        const final_text_header_object = structure.svg
            .append('text')
            .attr('x', 0)
            .attr('y', 70 * line_inst - 2)
            .attr('fill','#4c72b0')
            .style('font-size', '1.0em')
            .attr('opacity', '0.0')
            .text(text_final_header);

        // Transition
        const displayTransition_i = d3.transition().delay(800*line_inst+500).duration(800);
        
        initial_text_header_object.transition(displayTransition_i)
            .style('opacity', '0.0');
        final_text_header_object.transition(displayTransition_i)
            .style('opacity', '1.0');

        // Loop through individual tokens
        var individaul_line = text_lines[line_inst];
        for (var token_number in individaul_line)
        {
            // Calc color
            var default_color;
            if (reverse){
                // See if one element is in another
                if (text_lines_after[line_inst].includes(text_lines[line_inst][token_number])){
                    default_color = '#ebeed7';
                } else {
                    default_color = '#ae1e2f';
                }
            } else {
                // See if one element is in another
                if (text_lines[line_inst].includes(text_lines_after[line_inst][token_number])){
                    default_color = '#ebeed7';
                } else {
                    default_color = '#ae1e2f';
                }
            }
            

            // Reverse color logic
            var init_color;
            var final_color;
            if (reverse){
                init_color=default_color;
                final_color='#ebeed7';
            } else {
                init_color='#ebeed7';
                final_color=default_color;
            }

            // Add lines
            const initial_text_object = structure.svg
                .append('text')
                .attr('x', 175 + 135*token_number)
                .attr('y', 70 * line_inst)
                .attr('fill',init_color)
                .style('font-size', '1.375em')
                .text(text_lines[line_inst][token_number]);
            const final_text_object = structure.svg
                .append('text')
                .attr('x', 175 + 135*token_number)
                .attr('y', 70 * line_inst)
                .attr('fill',final_color)
                .style('font-size', '1.375em')
                .attr('opacity', '0.0')
                .text(text_lines_after[line_inst][token_number]);

            // Transitions    
            initial_text_object.transition(displayTransition_i)
                .style('opacity', '0.0');
            final_text_object.transition(displayTransition_i)
                .style('opacity', '1.0');

        }
    }
    
  
  }
// Define strings
const text_init_header = 'Before Tokenization';
const text_lines = [
    ['A broom is drearily sweeping','','','','',''],
    ['Up the broken pieces of yesterdays life','','','','',''], 
    ['Somewhere a queen is weeping','','','','',''],
    ['Somewhere a king has no wife','','','','',''],
    ['And the wind, it cries Mary','','','','','']
];
const text_final_header = 'After Tokenization';
const text_lines_after = [
    ['A', 'broom', 'is', 'drearily', 'sweeping'],
    ['Up', 'the', 'broken', 'pieces', 'of', 'yesterdays', 'life'],
    ['Somewhere', 'a', 'queen', 'is', 'weeping'],
    ['Somewhere', 'a', 'king', 'has', 'no', 'wife'],
    ['And', 'the', 'wind', ',', 'it', 'cries', 'Mary']
];

drawChart(text_init_header, text_lines, text_final_header, text_lines_after);
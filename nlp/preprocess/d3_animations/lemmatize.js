// Define strings
const text_init_header = 'Before Lemmatization';
const text_lines = [
    ['broom', 'drearily', 'sweeping'],
    ['broken', 'pieces', 'yesterdays', 'life'],
    ['somewhere', 'queen', 'weeping'],
    ['somewhere', 'king', 'wife'],
    ['wind', 'cries', 'mary']
];
const text_final_header = 'After Lemmatization';
const text_lines_after = [
    ['broom', 'drearily', 'sweep'],
    ['break', 'piece', 'yesterday', 'life'],
    ['somewhere', 'queen', 'weep'],
    ['somewhere', 'king', 'wife'],
    ['wind', 'cry', 'mary']  
];

drawChart(text_init_header, text_lines, text_final_header, text_lines_after);

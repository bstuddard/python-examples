// Define strings
const text_init_header = 'Before Stemming';
const text_lines = [
    ['broom', 'drearily', 'sweeping'],
    ['broken', 'pieces', 'yesterdays', 'life'],
    ['somewhere', 'queen', 'weeping'],
    ['somewhere', 'king', 'wife'],
    ['wind', 'cries', 'mary']
];
const text_final_header = 'After Stemming';
const text_lines_after = [
    ['broom', 'drearili', 'sweep'],
    ['broken', 'piec', 'yesterday', 'life'],
    ['somewher', 'queen', 'weep'],
    ['somewher', 'king', 'wife'],
    ['wind', 'cri', 'mari']
];

drawChart(text_init_header, text_lines, text_final_header, text_lines_after);

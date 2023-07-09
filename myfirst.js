const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question('Як тебе звати?', (answer1) => {
    rl.question(' Скільки тобі років? ', (answer2) => {
        rl.question('Чи є в тебе брати та сестри?', (answer3) => {
            console.log(`Ваші відповіді:\n1. ${answer1}\n2. ${answer2}\n3. ${answer3}`);
            rl.close();
        });
    });
});


import { faker } from "@faker-js/faker";

const enterKey = (win) => {
  if (win.document.activeElement) {
    cy.wrap(win.document.activeElement).type("{enter}", { force: true });
  } else {
    cy.get("body").type("{enter}", { force: true });
  }
};

const tabKey = (win) => {
  if (win.document.activeElement) {
    cy.wrap(win.document.activeElement).tab().focus();
  } else {
    cy.get("body").tab().focus();
  }
};

const typeKey = (win, randomFn) => {
  const chars =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  const input = chars.charAt(randomFn(0, chars.length - 1));
  if (win.document.activeElement) {
    cy.wrap(win.document.activeElement).type(input, { force: true });
  } else {
    cy.get("body").type(input, { force: true });
  }
  return input;
};

const typeSpecialKey = (win, randomFn) => {
  const specialKeys = [
    "{{}",
    "{backspace}",
    "{del}",
    "{downarrow}",
    "{end}",
    "{esc}",
    "{home}",
    "{leftarrow}",
    "{pagedown}",
    "{pageup}",
    "{rightarrow}",
    "{selectall}",
    "{uparrow}",
  ];
  const spkIndex = randomFn(0, specialKeys.length - 1);

  const modifiers = ["{alt}", "{ctrl}", "{meta}", "{shift}", ""];
  const modIndex = randomFn(0, modifiers.length - 1);

  let input = modifiers[modIndex] + specialKeys[spkIndex];
  if (win.document.activeElement) {
    cy.wrap(win.document.activeElement).type(input, { force: true });
  } else {
    cy.get("body").type(input, { force: true });
  }
  return input;
};

Cypress.Commands.add(
  "rKeypress",
  { prevSubject: true },
  (win, randomFn, callback) => {
    const actions = [
      () => enterKey(win),
      () => tabKey(win),
      () => typeKey(win, randomFn),
      () => typeSpecialKey(win, randomFn),
    ];
    const names = ["enter", "tab", "type", "special key"];
    const index = randomFn(0, actions.length - 1);
    const input = actions[index]();
    callback({
      title: "Keypress",
      value: {
        type: names[index],
        input,
      },
    });
  }
);

Cypress.Commands.add("rInput", (randomFn, callback) => {
  const actionBytype = {
    email: faker.internet.email,
    date: () => faker.date.anytime().toISOString().split("T")[0],
    tel: faker.phone.number,
    url: faker.internet.url,
    number: faker.number.int,
    text: faker.lorem.sentence,
    password: faker.internet.password,
  };

  // Esperar a que exista al menos un input en el DOM
  cy.get('body', { timeout: 10000 }).should('exist');
  
  cy.document().then((doc) => {
    const $inputs = Cypress.$("input", doc);
    if (!$inputs.length) {
      cy.log("⚠️ No se encontraron inputs en el DOM. Acción omitida.");
      callback({
        title: "Input",
        value: null,
        skipped: true
      });
      return;
    }
    const $visibleCandidates = $inputs.filter(
      (_i, candidate) => !Cypress.dom.isHidden(candidate)
    );
    if (!$visibleCandidates.length) {
      cy.log("⚠️ No hay inputs visibles. Acción omitida.");
      callback({
        title: "Input",
        value: null,
        skipped: true
      });
      return;
    }
    const index = randomFn(0, $visibleCandidates.length - 1);
    const $element = $visibleCandidates[index];
    const elementType = $element.getAttribute("type") || "text";
    const generator = actionBytype[elementType] || actionBytype.text;
    const inputValue = generator();
    cy.wrap($element, { log: false })
      .clear({ force: true })
      .type(`${inputValue}`, { force: true, delay: 0 })
      .then(() => {
        callback({
          title: "Input",
          value: {
            type: elementType,
            input: inputValue,
          },
        });
      });
  });
});



import io.github.bonigarcia.wdm.WebDriverManager;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.devtools.DevTools;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.slf4j.Logger;

import java.awt.*;
import java.awt.event.KeyEvent;
import java.time.Duration;

import static java.lang.invoke.MethodHandles.lookup;
import static org.slf4j.LoggerFactory.getLogger;

public class LeetcodeScraperTest {
    static final Logger log = getLogger(lookup().lookupClass());

    WebDriver driver;
    DevTools devTools;
    WebDriverWait wait;
    boolean firstPassIncomplete = true;

    @BeforeEach
    void setup() {
        driver = WebDriverManager.chromedriver().create();
        devTools = ((ChromeDriver) driver).getDevTools();
        devTools.createSession();
    }

    @AfterEach
    void teardown() {
        devTools.close();
        driver.quit();
    }

    @Test
    void leetScrape() throws InterruptedException, AWTException {
        login();
        Thread.sleep(3000);

        driver.get("https://leetcode.com/problems/two-sum");

        wait = new WebDriverWait(driver, Duration.ofSeconds(7));
        JavascriptExecutor js = (JavascriptExecutor) driver;
        Robot robot = new Robot();
        WebElement solution;

        for(int i = 0; i < 400; i++) {
            Thread.sleep(5000);
            try {
                solution = driver.findElement(By.cssSelector("div[data-key=solution]"));
                solution.click();
                wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("side-tools-wrapper__1TS9")));
                wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("content__QRGW")));

                //Once the code editor has been removed it will stay that way on following pages
                //Any further attempts to access it will lead to error
                if (firstPassIncomplete) {
                    wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("editor-wrapper__1ru6")));
                    js.executeScript("document.getElementsByClassName(\"editor-wrapper__1ru6\")[0].remove();");
                }

                js.executeScript("document.getElementsByClassName(\"side-tools-wrapper__1TS9\")[0].style.flex = 1;");
                long eltHeight = (long) js.executeScript("return document.getElementsByClassName(\"content__QRGW\")[0].scrollHeight;");

                js.executeScript(String.format("document.getElementsByClassName(\"layout__3fIJ\")[0].style.height = \"%dpx\"", eltHeight));

                robot.keyPress(KeyEvent.VK_CONTROL);
                robot.keyPress(KeyEvent.VK_S);
                robot.keyRelease(KeyEvent.VK_CONTROL);
                robot.keyRelease(KeyEvent.VK_S);

                Thread.sleep(1000L);

                if (firstPassIncomplete) {
                    setupDownloadSettings();
                }

                robot.keyPress(KeyEvent.VK_ENTER);
                robot.keyRelease(KeyEvent.VK_ENTER);

                Thread.sleep(1000);
            }
            catch (TimeoutException t) {
                driver.findElement(By.cssSelector("button[data-cy=next-question-btn]")).click();
                continue;
            }
            driver.findElement(By.cssSelector("button[data-cy=next-question-btn]")).click();
        }
    }

    void setupDownloadSettings() throws InterruptedException, AWTException {
        Robot robot = new Robot();

        Thread.sleep(1000L);

        robot.keyPress(KeyEvent.VK_SHIFT);
        robot.keyPress(KeyEvent.VK_TAB);
        robot.keyRelease(KeyEvent.VK_TAB);
        robot.keyPress(KeyEvent.VK_TAB);
        robot.keyRelease(KeyEvent.VK_TAB);
        robot.keyRelease(KeyEvent.VK_SHIFT);

        Thread.sleep(1000L);

        robot.keyPress(KeyEvent.VK_UP);
        robot.keyRelease(KeyEvent.VK_UP);

        Thread.sleep(1000L);
        robot.keyPress(KeyEvent.VK_TAB);
        robot.keyRelease(KeyEvent.VK_TAB);
        robot.keyPress(KeyEvent.VK_TAB);
        robot.keyRelease(KeyEvent.VK_TAB);
        robot.keyPress(KeyEvent.VK_TAB);
        robot.keyRelease(KeyEvent.VK_TAB);
        robot.keyPress(KeyEvent.VK_TAB);
        robot.keyRelease(KeyEvent.VK_TAB);

        robot.keyPress(KeyEvent.VK_ENTER);
        robot.keyRelease(KeyEvent.VK_ENTER);

        Thread.sleep(1000L);

        robot.keyPress(KeyEvent.VK_CONTROL);
        robot.keyPress(KeyEvent.VK_S);
        robot.keyRelease(KeyEvent.VK_CONTROL);
        robot.keyRelease(KeyEvent.VK_S);

        Thread.sleep(1000);
        firstPassIncomplete = false;
    }
    void login() throws InterruptedException {
        String username = "";
        String password = "";
        String startQuestionURL = "https://leetcode.com/accounts/login/";
        driver.get(startQuestionURL);

        wait = new WebDriverWait(driver, Duration.ofSeconds(20));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("signin_btn")));

        driver.findElement(By.id("id_login"))
                .sendKeys(username);
        Thread.sleep(500);
        driver.findElement(By.id("id_password"))
                .sendKeys(password);
        Thread.sleep(500);
        driver.findElement(By.id("signin_btn"))
                .click();
    }
}

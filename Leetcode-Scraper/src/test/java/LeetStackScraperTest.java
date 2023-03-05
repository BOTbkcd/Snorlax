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
import java.awt.datatransfer.Clipboard;
import java.awt.datatransfer.StringSelection;
import java.awt.event.KeyEvent;
import java.time.Duration;
import java.util.List;

import static java.lang.invoke.MethodHandles.lookup;
import static org.slf4j.LoggerFactory.getLogger;

public class LeetStackScraperTest {
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
        String URL = "https://leetcode.com/accounts/login/";
        driver.get(URL);

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

    @Test
    void stackSave() throws InterruptedException, AWTException {
        login();
        Thread.sleep(3000);

        driver.get("https://leetcode.com/explore/learn/card/fun-with-arrays/521/introduction/3221/");

        wait = new WebDriverWait(driver, Duration.ofSeconds(2013
        ));
        JavascriptExecutor js = (JavascriptExecutor) driver;
        Robot robot = new Robot();

        wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(".chapter-base.false")));

        js.executeScript("$(\".chapter-base.false\").click()");
        List<WebElement> items = driver.findElements(By.cssSelector(".accessible"));

        for(int i = 1; i <= items.size(); i++) {
            items.get(i-1).click();
            Thread.sleep(5000);

            String text = String.valueOf(i);
            StringSelection stringSelection = new StringSelection(text);
            Clipboard clipboard = Toolkit.getDefaultToolkit().getSystemClipboard();
            clipboard.setContents(stringSelection, stringSelection);

            try {
                robot.keyPress(KeyEvent.VK_CONTROL);
                robot.keyPress(KeyEvent.VK_S);
                robot.keyRelease(KeyEvent.VK_CONTROL);
                robot.keyRelease(KeyEvent.VK_S);

                Thread.sleep(1000L);

                if (firstPassIncomplete) {
                    setupDownloadSettings();
                }

                robot.keyPress(KeyEvent.VK_CONTROL);
                robot.keyPress(KeyEvent.VK_V);
                robot.keyRelease(KeyEvent.VK_V);
                robot.keyRelease(KeyEvent.VK_CONTROL);


                robot.keyPress(KeyEvent.VK_ENTER);
                robot.keyRelease(KeyEvent.VK_ENTER);

                Thread.sleep(1000);
            }
            catch (TimeoutException t) {
                continue;
            }
        }
    }
}

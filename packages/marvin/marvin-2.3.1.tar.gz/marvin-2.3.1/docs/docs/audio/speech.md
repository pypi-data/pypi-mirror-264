# Generating speech

Marvin can generate speech from text. 

<div class="admonition abstract">
  <p class="admonition-title">What it does</p>
  <p>
    The <code>speak</code> function generates audio from text. The <code>@speech</code> decorator generates speech from the output of a function.
  </p>
</div>



!!! example
    === "From a string"

        The easiest way to generate speech is to provide a string:
        
        ```python
        import marvin

        audio = marvin.speak("I sure like being inside this fancy computer!")
        ```

        !!! success "Result"
            ```python
            audio.stream_to_file("fancy_computer.mp3")
            ```
            <audio controls>
              <source src="/assets/audio/fancy_computer.mp3" type="audio/mpeg">
              Your browser does not support the audio element.
            </audio>

        
    === "From a function"

        For more complex use cases, you can use the `@image` decorator to generate images from the output of a function:
        
        ```python
        @marvin.speech
        def say_hello(name: str):
            return f'Hello, {name}! How are you doing today?'
        

        audio = say_hello("Arthur")
        ```

        !!! success "Result"
            ```python
            audio.stream_to_file("hello_arthur.mp3")
            ```
            <audio controls>
              <source src="/assets/audio/hello_arthur.mp3" type="audio/mpeg">
              Your browser does not support the audio element.
            </audio>

<div class="admonition info">
  <p class="admonition-title">How it works</p>
  <p>
    Marvin passes your prompt to the OpenAI speech API, which returns an audio file.
  </p>
</div>

## Speaking text verbatim

Unlike the images API, OpenAI's speech API does not modify or revise your input prompt in any way. Whatever text you provide is exactly what will be spoken. 

Therefore, you can use the `speak` function to generate speech from any string, or use the `@speech` decorator to generate speech from the string output of any function.




## Generating speech
By default, OpenAI generates speech from the text you provide, verbatim. We can use Marvin functions to generate more interesting speech by modifying the prompt before passing it to the speech API. For example, we can use a function to generate a line of dialogue that reflects a specific intent. And because of Marvin's modular design, we can simply add a `@speech` decorator to the function to generate speech from its output.

```python
import marvin

@marvin.speech
@marvin.fn
def ai_say(intent: str) -> str:
    '''
    Given an `intent`, generate a line of diagogue that 
    reflects the intent / tone / instruction without repeating 
    it verbatim.
    '''
    
ai_say('hello') 
# Hi there! Nice to meet you.
```

!!! success "Result"
    <audio controls>
      <source src="/assets/audio/ai_say.mp3" type="audio/mpeg">
      Your browser does not support the audio element.
    </audio>

## Choosing a voice

Both `speak` and `@speech` accept a `voice` parameter that allows you to choose from a variety of voices. You can preview the available voices [here](https://platform.openai.com/docs/guides/text-to-speech/voice-options).

```python

## Saving audio files

The result of the `speak` function and `@speech` decorator is an audio stream. You can save this stream to disk like this:

```python
audio = marvin.speak("Hello, world!")
audio.stream_to_file("hello_world.mp3")
```


## Model parameters
You can pass parameters to the underlying API via the `model_kwargs` arguments of `speak` and `@speech`. These parameters are passed directly to the respective APIs, so you can use any supported parameter.


## Async support

If you are using Marvin in an async environment, you can use `speak_async` (or decorate an async function with `@speech`) to generate speech asynchronously:

```python
result = await marvin.speak_async('I sure like being inside this fancy computer!')
```
